import requests
import json
import threading

debug = False


def print_d(*args):
    if debug:
        print(*args)


class HttpClient():

    def __init__(self, endpoint, device_token, ctx=None):
        self.token = device_token
        self.ctx = ctx
        self.connected = False
        if ctx is not None:
            self.endpoint = "https://" + endpoint
        else:
            self.endpoint = "http://" + endpoint

    def connect(self):
        try:
            res = requests.get(self._attributes_url() + '/updates?timeout=1000', ctx=self.ctx)
            if res.status == 200 or res.status == 408:
                self.connected = True
                return True
        except Exception as e:
            print_d("connect", e)
            self.connected = False
            return False
        print_d("connect failed", res.status)
        self.connected = False
        return False

    def is_connected(self):
        return self.connected

    def on_rpc_request(self, id, method, params):
        pass

    def _do_loop(self):
        while True:
            try:
                rpc = self._get_rpc_request()
                if rpc is not None:
                    self.on_rpc_request(rpc['id'], rpc['method'], rpc['params'])
            except Exception as e:
                print_d("http loop", e)
                sleep(5000)

    def loop(self):
        thread(self._do_loop)

    def _telemetry_url(self):
        return self.endpoint + "/api/v1/" + self.token + "/telemetry"

    def _attributes_url(self):
        return self.endpoint + "/api/v1/" + self.token + "/attributes"

    def _rpc_url(self, id=None):
        if id is not None:
            return self.endpoint + "/api/v1/" + self.token + "/rpc/" + str(id)
        return self.endpoint + "/api/v1/" + self.token + "/rpc"

    def publish_telemetry(self, values, ts=None):
        if ts is not None:
            values = {'values': values, 'ts': ts}
        try:
            res = requests.post(self._telemetry_url(), json=values, ctx=self.ctx)
        except Exception as e:
            print_d(e)
            return False
        if res.status != 200:
            return False
        return True

    def publish_attributes(self, client):
        try:
            res = requests.post(self._attributes_url(), json=client, ctx=self.ctx)
        except Exception as e:
            print_d(e)
            return False
        if res.status != 200:
            return False
        return True

    def get_attributes(self, client, shared=None, timeout=20000):
        obj = {}
        if client and isinstance(client, PSTRING):
            obj['clientKeys'] = client
        else:
            client = None
        if shared and isinstance(shared, PSTRING):
            obj['sharedKeys'] = shared
        else:
            shared = None
        try:
            res = requests.get(self._attributes_url(), params=obj, ctx=self.ctx)
            if res.status != 200:
                return None
            obj = json.loads(res.content)
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

    def _get_rpc_request(self, timeout=20000):
        obj = {'timeout': timeout}
        try:
            res = requests.get(self._rpc_url(), params=obj, ctx=self.ctx)
            if res.status != 200:
                return None
            obj = json.loads(res.content)
            self.connected = True
            return obj
        except Exception as e:
            print_d(e)
            self.connected = False
            return None

    def publish_rpc_reply(self, id, result):
        try:
            res = requests.post(self._rpc_url(id), json=result, ctx=self.ctx)
        except Exception as e:
            print_d(e)
            return False
        if res.status != 200:
            return False
        return True
