"""
.. module:: iot

********************
Fortebit IoT Library
********************

The Zerynth Fortebit IoT Library can be used to ease the connection to the `Fortebit IoT Cloud <https://fortebit.tech/cloud/>`_.

It makes your device act as a Fortebit IoT Device that can be monitored and controlled on the Fortebit IoT Cloud dashboard.

The device always send and receive data in the JSON format.

    """


class Device():
    """
================
The Device class
================

.. class:: Device(device_token, client, ctx=None)

        Create a Device instance representing a Fortebit IoT device.

        The device is provisioned by the :samp:`device_token`, obtained from the Fortebit dashboard upon the creation of a new device.
        The :samp:`client` parameter is a class that provides the implementation of the low level details for the connection.
        It can be one of :samp:`MqttClient` in the :samp:`mqtt_client` module, or :samp:`HttpClient` in the :samp:`http_client` module.
        The optional :samp:`ctx` parameter is an initialized secure socket context.

    """

    def __init__(self, device_token, client, ctx=None):
        self.device_token = device_token
        self.endpoint = "cloud.fortebit.tech"
        self.client = client(self.endpoint, device_token, ctx)

    def listen_rpc(self, callback):
        """
.. method:: listen_rpc(callback)

        Listen to incoming RPC requests that get reported to the specified :samp:`callback` function,
        called as *callback(id, method, params)*:
        
        * :samp:`id` is the request identifier (number)
        * :samp:`method` is the method identifier of the RPC (Remote Procedure Call)
        * :samp:`params` is a dictionary containing the RPC method arguments (or parameters)
        
        Call :func:`send_rpc_reply` to provide the result of the RPC request.
        
        """
        self.client.on_rpc_request = callback

    def connect(self, retry=7):
        """
.. method:: connect()

        Setup a connection to the Fortebit Cloud. Return *True* if successful.

        """
        return self.client.connect()

    def is_connected(self):
        """
.. method:: is_connected()

        Returns the status of the connection to the Fortebit Cloud (reconnections are automatic).

        """
        return self.client.is_connected()

    def run(self):
        """
.. method:: run()

        Starts the device by executing the underlying client loop.

        """
        self.client.loop()

    def publish_telemetry(self, values, ts=None):
        """
.. method:: publish_telemetry(values, ts)

        Publish :samp:`values` (dictionary) to the device telemetry, with optional timestamp :samp:`ts` (epoch in milliseconds).

        Return a boolean, *False* if the message cannot be sent.
        """
        return self.client.publish_telemetry(values, ts)

    def publish_attributes(self, attributes):
        """
.. method:: publish_attributes(attributes)

        Publish :samp:`attributes` (dictionary) to the device *client* attributes.

        Return a boolean, *False* if the message cannot be sent.
        """
        return self.client.publish_attributes(attributes)

    def get_attributes(self, client, shared=None, timeout=10000):
        """
.. method:: get_attributes(client, shared, timeout)

        Obtain the specified :samp:`client` and/or :samp:`shared` attributes from the device.

        Return a dictionary, *None* if the data could not be received.
        """
        return self.client.get_attributes(client, shared, timeout)

    def send_rpc_reply(self, id, result):
        """
.. method:: send_rpc_reply(id, result)

        Publish :samp:`result` (dictionary) as a reply to the RPC request with identifier :samp:`id`.

        Return a boolean, *False* if the message cannot be sent.
        """
        return self.client.send_rpc_reply(id, result)

    def do_rpc_request(self, method, params=None, timeout=15000):
        """
.. method:: do_rpc_request(method, params, timeout)

        Perform an RPC request with name :samp:`method` and arguments :samp:`params`, waiting for
        a reply maximum :samp:`timeout` milliseconds (only with MqttClient).

        Return the result of the RPC (dictionary), *None* in case of errors.
        """
        return self.client.do_rpc_request(method, params, timeout)
