from lwmqtt import mqtt
import json
import streams
import threading
import mcu

debug = False


def print_d(*args):
    if debug:
        print(*args)


class MqttClient():

    def __init__(self, endpoint, device_token, ctx=None):
        self.endpoint = endpoint
        self.ctx = ctx
        self.driver = mqtt.Client("polaris", True)
        self.driver.set_username_pw(device_token)
        self.attr_id = -1
        self.attr_ev = threading.Event()
        self.attr_obj = None
        self.rpc_id = 10000
        self.rpc_ev = threading.Event()
        self.rpc_obj = None

    def _loop_failure(self, client):
        while True:
            try:
                print_d("> reconnecting...")
                client.reconnect()
                break
            except Exception as e:
                print_d(e)
            sleep(10000)
        return mqtt.RECOVERED

    def _subscribe_cb(self, client):
        # subscribe to attributes
        client.subscribe("v1/devices/me/attributes/response/+", self._on_attributes, 1)
        client.subscribe("v1/devices/me/rpc/request/+", self._on_rpc_request, 1)
        client.subscribe("v1/devices/me/rpc/response/+", self._on_rpc_response, 1)


    def connect(self):
        port = 1883 if self.ctx is None else 8883
        try:
            self.driver.connect(self.endpoint, 60, port=port, ssl_ctx=self.ctx,
                                loop_failure=self._loop_failure, aconnect_cb=self._subscribe_cb, start_loop=False)
        except Exception as e:
            print_d("failed", e)
            return False
        return True

    def is_connected(self):
        return self.driver.connected()

    def loop(self):
        self.driver.loop()

    def _on_attributes(self, client, payload, topic):
        print_d("> got:", topic, payload)
        # len("v1/devices/me/attributes/response/") = 34
        id = int(topic[34:])
        if self.attr_id == id:
            self.attr_obj = json.loads(payload)
            self.attr_ev.set()

    def on_rpc_request(self, id, method, params):
        pass

    def _on_rpc_request(self, client, payload, topic):
        print_d("> got:", topic, payload)
        # len("v1/devices/me/rpc/request/") = 26
        id = int(topic[26:])
        obj = json.loads(payload)
        self.on_rpc_request(id, obj['method'], obj['params'] if 'params' in obj else None)

    def get_attributes(self, client, shared=None, timeout=10000):
        self.attr_id += 1
        self.attr_ev.clear()
        obj = {}
        if client and isinstance(client, PSTRING):
            obj['clientKeys'] = client
        else:
            client = None
        if shared and isinstance(shared, PSTRING):
            obj['sharedKeys'] = shared
        else:
            shared = None
        obj = json.dumps(obj)
        ep = 'v1/devices/me/attributes/request/' + str(self.attr_id)
        print_d("publish:", ep, obj)
        try:
            self.driver.publish(ep, obj, qos=1)
            obj = None
            self.attr_ev.wait(timeout)
            obj = self.attr_obj
        except Exception as e:
            print_d(e)
            return None
        if obj is None:
            return None
        if 'client' in obj:
            client = obj['client']
        else:
            client = None
        if 'shared' in obj:
            shared = obj['shared']
        else:
            shared = None
        return (client, shared)

    def publish_attributes(self, attributes):
        try:
            self.driver.publish('v1/devices/me/attributes', json.dumps(attributes), qos=1)
        except Exception as e:
            print_d(e)
            return False
        return True

    def publish_telemetry(self, values, ts=None):
        if ts is not None:
            values = {'values': values, 'ts': ts}
        try:
            self.driver.publish('v1/devices/me/telemetry', json.dumps(values), qos=1)
        except Exception as e:
            print_d(e)
            return False
        return True

    def send_rpc_reply(self, id, result):
        print_d("rpc reply", id, result)
        try:
            self.driver.publish('v1/devices/me/rpc/response/' + str(id), json.dumps(result), qos=1)
        except Exception as e:
            print_d(e)
            return False
        return True

    def _on_rpc_response(self, client, payload, topic):
        print_d("> got:", topic, payload)
        # len("v1/devices/me/rpc/response/") = 27
        id = int(topic[27:])
        if self.rpc_id == id:
            self.rpc_obj = json.loads(payload)
            self.rpc_ev.set()

    def do_rpc_request(self, method, params=None, timeout=15000):
        self.rpc_id += 1
        self.rpc_ev.clear()
        print_d("rpc request:", self.rpc_id, method, params)
        try:
            msg = { 'method': method, 'params': params }
            self.driver.publish('v1/devices/me/rpc/request/' + str(self.rpc_id), json.dumps(msg), qos=1)
            obj = None
            self.rpc_ev.wait(timeout)
            obj = self.rpc_obj
        except Exception as e:
            print_d(e)
            return None
        return obj
