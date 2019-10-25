"""
.. module:: cloud

*************
Polaris Cloud
*************

This module provides easy access to the Fortebit Cloud features.

    """

import requests


def getAccessToken(imei, uid):
    """
.. function:: getAccessToken(imei, uid)

    Generates the board's own access token for Fortebit IoT cloud services.

    :param imei: The modem IMEI number (as a 15 characters string)
    :param uid: The MCU unique identifier (as a 3 integers sequence)
    """
    import struct
    _cmap = 'bBcCdDeEfFgGkKmMnNpPrRsStTuUwWzZ'
    a = int(imei[0:8])
    b = int(imei[3:11])
    c = int(imei[6:14])
    #print(len(uid),[hex(i) for i in mcu.uid()])
    u = struct.unpack("<III", uid)
    a += u[0] - u[1]
    b += u[1] - u[2]
    c += u[2] - u[0]
    a &= 0xFFFFFFFF
    b &= 0xFFFFFFFF
    c &= 0xFFFFFFFF
    a = (a + (b * c)) & 0xFFFFFFFF
    a = (a ^ (a >> 14)) & 0xFFFFF
    b = ((a * b) + c) & 0xFFFFFFFF
    b = (b ^ (b >> 14)) & 0xFFFFF
    c = 'A'
    c += _cmap[a & 0x1F] + _cmap[(a >> 5) & 0x1F] + _cmap[(a >> 10) & 0x1F] + _cmap[(a >> 15) & 0x1F]
    c += _cmap[b & 0x1F] + _cmap[(b >> 5) & 0x1F] + _cmap[(b >> 10) & 0x1F] + _cmap[(b >> 15) & 0x1F]
    c += '_'
    for b in range(0, len(imei), 3):
        a = int(imei[b:b + 3])
        c += _cmap[a & 0x1F] + _cmap[(a >> 5) & 0x1F]
    return c


def isRegistered(device, email):
    """
.. function:: isRegistered(device, email)

    Check if the specified IoT device is registered to the Polaris Cloud services.

    :param device: a connected instance of :any:`fortebit.iot.Device`
    :param email: the device owner's email address
    """
    attributes = device.get_attributes(None, 'email')
    if attributes and attributes[1] and 'email' in attributes[1] and attributes[1]['email'] == email:
        return True
    return False


def register(device, email):
    """
.. function:: register(device, email)

    Perform device registration to Fortebit IoT cloud services.

    :param device: a connected instance of :any:`fortebit.iot.Device`
    :param email: the device owner's email address
    """
    obj = {"email": email, "token": device.device_token}
    print("Register device", obj)
    obj = device.do_rpc_request("register", obj)
    #print(obj)
    if obj and "reply" in obj and obj["reply"] == "OK":
        return True
    return False

# def register(device, email, imei, ssl_ctx=None):
#     """
# .. function:: register(device, email, imei, ssl_ctx)

#     Perform device registration to Fortebit IoT cloud services.

#     :param device: a connected instance of :any:`fortebit.iot.Device`
#     :param email: the device owner's email address
#     :param imei: the modem IMEI number (as a 15 characters string)
#     :param ssl_ctx: an optional SSL/TLS context (use HTTPS if present)
#     """
#     if ssl_ctx:
#         url = "https://"
#     else:
#         url = "http://"
#     url += device.endpoint + "/script-polaris/register"
#     obj = {"email": email, "token": device.device_token, "imei": imei}
#     print("Register device", email, device.device_token, url, obj)
#     try:
#         res = requests.get(url, params=obj, ctx=ssl_ctx)
#         if res.status == 200:
#             return True
#         print("Registration error", res.status)
#     except Exception as e:
#         print(e)
#     return False
