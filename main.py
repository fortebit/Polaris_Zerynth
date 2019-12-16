
# POLARIS_FORTEBIT
# Created at 2019-07-26 11:34:26.282569

from fortebit.polaris import polaris
from fortebit.polaris import modem
from fortebit.polaris import gnss
import vm
import sfw
vm.set_option(vm.VM_OPT_RESET_ON_EXCEPTION, 1)
vm.set_option(vm.VM_OPT_TRACE_ON_EXCEPTION, 1)
vm.set_option(vm.VM_OPT_RESET_ON_HARDFAULT, 1)
vm.set_option(vm.VM_OPT_TRACE_ON_HARDFAULT, 1)
import streams
s = streams.serial()

import mcu
import timestamp
import timers
import ssl
import requests
import threading
from wireless import gsm
import utils

sleep(1000)

# CONFIG
poll_time = 100                     # poll inputs at twice the specified period in ms
gps_period = 10000                  # gps lat,lon and speed telemetry period in ms
update_period = 6 * gps_period      # other telemetry data period in ms
no_ignition_period = 300000         # no ignition telemetry data period in ms

fw_version = "1.11"

# POLARIS INIT
try:
    print("Polaris default app")
    polaris.init()
    
    print("MCU UID:", [hex(b) for b in mcu.uid()])
    print("VM info:", vm.info())
    print("FW version:", fw_version)
    print("Watchdog was triggered:", sfw.watchdog_triggered())
    
    polaris.ledRedOn()
    polaris.ledGreenOff()

except Exception as e:
    print("Failed polaris init with", e)
    sleep(500)
    mcu.reset()


# INIT HW

try:
    print("Initializing Modem...")
    modem = modem.init()
    print("Initializing GNSS...")
    gnss = gnss.init()
    # verify preconditions and start utility thread
    utils.start()

    print("Starting Accelerometer...")
    import accel
    accel.start()
    print("Starting GNSS...")
    gnss.start()
    gnss.set_rate(2000)

    print("Starting Modem...")
    modem.startup()
    
    # enable modem/gnss utilities
    utils.modem = modem
    utils.gnss = gnss

    sfw.watchdog(0, 30000)
    sfw.kick()
    if utils.check_terminal(s):
        utils.do_terminal(s)

    minfo = gsm.mobile_info()
    print("Modem:", minfo)
    
    # enable SMS checking
    utils.check_sms = True
except Exception as e:
    print("Failed init hw with", e)
    sleep(500)
    mcu.reset()


# GATHERING SETTINGS
name = None
apn = None
email = None

try:
    print("Read settings...")
    settings = utils.readSettings()
    sfw.kick()

    if "apn" in settings:
        apn = settings["apn"]
        print("APN:", apn)

    if "email" in settings:
        email = settings["email"]
        print("Email:", email)

    if "name" in settings:
        name = settings["name"]
        print("Name:", name)

    if apn is not None and not utils.validate_apn(apn):
        print("Invalid APN!")
        apn = None
    if email is not None and not utils.validate_email(email):
        print("Invalid email!")
        email = None
    if name is None:
        name = "Polaris"
        print("Saving name:", name)
        settings["name"] = name
        utils.saveSettings(settings)
    if apn is None:
        print("APN is not defined, can't connect to Internet!")
        apn = utils.request_apn(s)
        print("Saving APN:", apn)
        settings["apn"] = apn
        utils.saveSettings(settings)
    if email is None:
        print("email is not defined, can't register to Cloud!")
        email = utils.request_email(s)
        print("Saving email:", email)
        settings["email"] = email
        utils.saveSettings(settings)
except Exception as e:
    print("Failed gathering settings with", e)
    sleep(500)
    mcu.reset()


# GSM ATTACH
try:
    print("Waiting for network...",end='')
    for _ in range(150):
        sfw.kick()
        ninfo = gsm.network_info()
        if ninfo[6]:
            break
        sleep(1000)
        if (_ % 10) == 9:
            print('.',end='')
    else:
        raise TimeoutError
    print("ok!")
    print("Attached to network:", ninfo)

    print("Activating data connection...")
    for _ in range(3):
        try:
            gsm.attach(apn)
            break
        except Exception as e:
            print("Retrying...", e)
        try:
            gsm.detach()
            sleep(5000 * (_ + 1))
        except:
            pass
    else:
        raise TimeoutError
    linfo = gsm.link_info()
    print("Connection parameters:", linfo)
except Exception as e:
    print("Network failure", e)
    sleep(500)
    mcu.reset()


# FORTEBIT CLOUD
try:
    from fortebit.polaris import cloud
    # get access token
    device_token = cloud.getAccessToken(minfo[0], mcu.uid())
    # NOTE! Do not disclose security token in production builds
    print("Access Token:", device_token)

    print("Connecting to Fortebit Cloud...")
    # retrieve the CA certificate used to sign the howsmyssl.com certificate
    cacert = __lookup(SSL_CACERT_DST_ROOT_CA_X3)
    # create a SSL context to require server certificate verification
    ctx = ssl.create_ssl_context(cacert=cacert, options=ssl.CERT_REQUIRED | ssl.SERVER_AUTH)
    # NOTE: if the underlying SSL driver does not support certificate validation
    #       uncomment the following line!
    # ctx = None
    
    from fortebit.iot import iot
    from fortebit.iot import mqtt_client
    # from fortebit.iot import http_client
    # let's create a device passing the token and the type of client
    device = iot.Device(device_token, mqtt_client.MqttClient, ctx)  # use ctx for TLS
    # device = iot.Device(device_token, http_client.HttpClient, ctx)  # use ctx for TLS
    
    utils.client = device.client

    # connect the device
    if not device.connect():
        for _ in range(5):
            sfw.kick()
            try:
                sleep(3000 * (_ + 1))
                print("Retrying...")
                if device.connect():
                    break
            except Exception as e:
                print("Failed connect...", e)
        else:
            raise TimeoutError

    print("Device is connected")
    polaris.ledGreenOn()

    # start the device
    device.run()
    sfw.kick()
    print("Device is up and running")

    # if not registered, register device to Fortebit Cloud
    if not cloud.isRegistered(device, email):
        sfw.kick()
        retry = timers.now()
        print("Device is not registered, register device...")
        while timers.now() - retry < 60000:
            if cloud.register(device, email):
                sfw.kick()
                if cloud.isRegistered(device, email):
                    break
            if not device.is_connected():
                raise ConnectionError
            sleep(5000)
            print("Retry device registration...")
        else:
            raise TimeoutError

    sfw.kick()
    print("Device is registered")
    polaris.ledRedOff()
    polaris.ledGreenOff()
    print("Publish device attributes")
    device.publish_attributes({"name": name,
                              "target_board": vm.info()[1].upper(),
                              "vm_version": vm.info()[2],
                              "fw_version": fw_version})
    sfw.kick()

except Exception as e:
    print("Failed access to Fortebit cloud", e)
    sleep(500)
    mcu.reset()

# TELEMETRY LOOP
try:
    accel.get_sigma()  # reset accumulated value
    sleep(500)

    last_time = -(no_ignition_period + gps_period) # force sending data immediately
    counter = 0
    sos = -1
    connected = True
    ignition = None
    sos = None
    telemetry = {}
    disconn_time = None

    while True:
        # allow other threads to run while waiting
        sleep(poll_time*2)
        sfw.kick()
        now_time = timers.now()

        if utils.check_terminal(s):
            utils.do_terminal(s)

        # read inputs
        old_ign = ignition
        ignition = polaris.getIgnitionStatus()
        old_sos = sos
        sos = polaris.getEmergencyStatus()
        extra_send = False

        if connected and not device.is_connected():
            if disconn_time is None:
                disconn_time = now_time + 60000 # add some time to recover
            connected = False
        elif not connected and device.is_connected():
            connected = True
            disconn_time = None

        if not connected and disconn_time:
            if now_time > disconn_time:
                raise TimeoutError
                pass

        # led waiting status
        utils.status_led(False, ignition, connected)

        if sos != old_sos:
            telemetry['sos'] = sos
            extra_send = True

        if ignition != old_ign:
            telemetry['ignition'] = ignition
            extra_send = True

        if not extra_send:
            if ignition == 0:
                # sleep as indicated by rate for no ignition
                if now_time - last_time < no_ignition_period - poll_time:
                    continue
                extra_send = True
            else:
                # sleep as indicated by rate
                if now_time - last_time < gps_period - poll_time:
                    continue

        ts = modem.rtc()
        #print("MODEM RTC =", ts)

        if counter % (update_period / gps_period) == 0 or extra_send:
            telemetry['ignition'] = ignition
            telemetry['sos'] = sos

            if polaris.isBatteryBackup():
                telemetry['charger'] = -1
            else:
                telemetry['battery'] = utils.decimal(3, polaris.readMainVoltage())
                telemetry['charger'] = polaris.getChargerStatus()

            telemetry['backup'] = utils.decimal(3, polaris.readBattVoltage())
            telemetry['temperature'] = utils.decimal(2, accel.get_temperature())
            telemetry['sigma'] = utils.decimal(3, accel.get_sigma())

            pr = accel.get_pitchroll()
            telemetry['pitch'] = utils.decimal(1, pr[0])
            telemetry['roll'] = utils.decimal(1, pr[1])

        if gnss.has_fix():
            fix = gnss.fix()
            # only transmit position when it's accurate
            if fix[6] < 2.5:
                telemetry['latitude'] = utils.decimal(6, fix[0])
                telemetry['longitude'] = utils.decimal(6, fix[1])
                telemetry['speed'] = utils.decimal(1, fix[3])
                if counter % (update_period / gps_period) == 0 or extra_send:
                    telemetry['altitude'] = utils.decimal(1, fix[2])
                    telemetry['COG'] = utils.decimal(1, fix[4])
            if counter % (update_period / gps_period) == 0 or extra_send:
                telemetry['nsat'] = fix[5]
                telemetry['HDOP'] = utils.decimal(2, fix[6])
            # replace timestamp with GPS
            ts = fix[9]
        elif ts is not None and ts[0] < 2019:
            ts = None

        if ts is not None:
            ts = str(timestamp.to_unix(ts)) + "000"

        counter += 1
        last_time = now_time

        # led sending status
        utils.status_led(True, ignition, connected)

        print("Publishing:", counter, ts, telemetry)
        sfw.kick()
        ok = device.publish_telemetry(telemetry, ts)
        telemetry = {}
        
        if not ok:
            print("Publishing failed") # TODO: retry or store to qspiflash and resend later

except Exception as e:
    print("Failed telemetry loop", e)
    sleep(500)
    mcu.reset()
