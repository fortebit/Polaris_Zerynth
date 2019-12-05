import mcu
import sfw
import pwr
import timers
import streams
import json
from fortebit.polaris import polaris
import accel

modem = None
gnss = None
client = None
check_sms = False

has_qspi = True

def decimal(n, v):
    v = float(v)
    s = "%%.%df" % n
    return s % v

# entry sequence is '+++' within 1 second
start_check = 0
count_check = 0

def check_terminal(s):
    global start_check, count_check
    while s.available() > 0:
        c = s.read()[0]
        if c == __ORD('+'):
            t = timers.now()
            count_check += 1
            if count_check == 1:
                start_check = t
            if t - start_check < 1000:
                if count_check == 3:
                    count_check = 0
                    return True
            else:
                start_check = t
                count_check = 1
        else:
            count_check = 0
    return False


def do_terminal(s):
    print("[Type +++ to exit terminal]")
    while True:
        print("Input command:")
        cmd = input_line(s)
        if cmd == '+++':
            break
        elif cmd == 'erase':
            eraseSettings()
            print("erase done")
            mcu.reset()
        elif cmd == 'name':
            settings = readSettings()
            print("Old name:", settings["name"])
            print("New name:")
            name = input_line(s)
            if name:
                print("Saving name:", name)
                settings["name"] = name
                saveSettings(settings)
                mcu.reset()
        elif cmd == 'modem':
            do_modem_passthru(s)
            break
        elif cmd == 'gnss':
            global gnss
            gnss.debug = not gnss.debug
            print("gnss debug =", gnss.debug)
            break
        elif cmd == 'mqtt':
            global client
            if client is not None:
                client.debug = not client.debug
                print("mqtt debug =", client.debug)
                break


def do_modem_passthru(s):
    print("Modem passthrough...[^ to exit]")
    modem.bypass(1)
    ms = streams.serial(polaris.gsm.SERIAL,baud=115200,set_default=False)
    ms.write('ATE1\r')
    while True:
        sfw.kick()
        # modem to stream
        n = ms.available()
        if n > 0:
            s.write(ms.read(n))
        # stream to modem
        n = s.available()
        if n > 0:
            b = s.read(n)
            if n == 1 and b[0] == __ORD('^'):
                break
            ms.write(b)
        else:
            sleep(1)
    ms.write('ATE0\r')
    modem.bypass(0)


def input_line(s):
    res = bytearray()
    s.read(s.available())
    while True:
        if s.available() < 1:
            sfw.kick()
            sleep(1)
            continue
        c = s.read()[0]
        if c == __ORD('\r') or c == __ORD('\n'):
            break
        if c == __ORD('\b') and len(res) > 0:
            del res[-1]
            print('\b ', sep='', end='')
        else:
            res.append(c)
        print(chr(c), sep='', end='')
    print()
    return str(res)


def validate_apn(apn):
    apn = bytes(apn)
    for c in apn:
        if not ((c >= __ORD('a') and c <= __ORD('z')) or (c >= __ORD('A') and c <= __ORD('Z'))
                or (c >= __ORD('0') and c <= __ORD('9')) or c == __ORD('-') or c == __ORD('.')):
            return False
    return True


def validate_email(email):
    email = bytes(email)
    dom = -1
    for c in email:
        if dom >= 0:
            if not ((c >= __ORD('a') and c <= __ORD('z')) or (c >= __ORD('A') and c <= __ORD('Z'))
                    or (c >= __ORD('0') and c <= __ORD('9')) or c == __ORD('-') or c == __ORD('.')):
                return False
            dom += 1
            if c == __ORD('.'):
                dom = 255
        else:
            if c >= 128:
                return False
            if c == __ORD('@'):
                dom = 0
    return len(email) > 2 and dom >= 256


def saveSettings(settings):
    if has_qspi:
        my_flash = polaris.QSpiFlash()
        my_flash.erase_block(0)
        my_flash[0] = json.dumps(settings) + "\n"


def readSettings():
    if has_qspi:
        my_flash = polaris.QSpiFlash()
        data = my_flash.read_data(0, 128)
        if not data.find("\n") < 0:
            return json.loads(data[0:data.find("\n")])
        else:
            return {}
    else:
        return {"apn": "tm", "email": "test@test.com"}


def eraseSettings():
    my_flash = polaris.QSpiFlash()
    my_flash.erase_block(0)


def read_and_parse_sms():
    mcu_reset = False
    sms = modem.list_sms(False,10,0)
    if sms and len(sms) > 0:
        for msg in sms:
            print("Index:", msg[3])
            print("Text:", msg[0])
            print("From:", msg[1])
            print("Time:", msg[2])
            modem.delete_sms(msg[3])
            text = msg[0].split(",")
            ret = ""
            for line in text:
                line = line.split("=")
                line[0] = line[0].lower().strip()
                if line[0] == "erase":
                    print('erase flash')
                    eraseSettings()
                    ret += "erase done"
                    mcu_reset = True
                if line[0] == "apn" and len(line) > 1:
                    line[1] = line[1].replace(" ", "")
                    apn = line[1]
                    print("APN", apn)
                    settings = readSettings()
                    settings["apn"] = apn
                    saveSettings(settings)
                    ret += "apn " + apn + " saved,"
                    mcu_reset = True
                if line[0] == "email" and len(line) > 1:
                    line[1] = line[1].replace(" ", "")
                    email = line[1]
                    print("email", email)
                    settings = readSettings()
                    settings["email"] = email
                    saveSettings(settings)
                    ret += "email " + email + " saved,"
                    mcu_reset = True
                if line[0] == "name" and len(line) > 1:
                    name = line[1].strip()
                    print("name", name)
                    settings = readSettings()
                    settings["name"] = name
                    saveSettings(settings)
                    ret += "name changed " + name + ","
                    mcu_reset = True
            if len(ret) > 0:
                if ret[-1] == ",":
                    ret = ret[0:-1]
                modem.send_sms(msg[1], ret)
    return mcu_reset


charging = False

def update_charger():
    global charging
    if polaris.isBatteryBackup():
        charging = False
    elif charging:
        if accel.get_temperature() < 4 or accel.get_temperature() > 45:
            print("Exceeding battery temperature range!")
            charging = False
        if not charging:
            print("Stop battery charging...")
    else:
        if accel.get_temperature() >= 6 and accel.get_temperature() <= 43:
            print("Good battery temperature range!")
            charging = True
        if charging:
            print("Start battery charging...")
    
    polaris.setBatteryCharger(charging)


def is_powersupply_toolow():
    if polaris.isBatteryBackup():
        volt = polaris.readBattVoltage()
        if volt < 3.45:
            print("Backup battery:", volt)
            return True
    else:
        volt = polaris.readMainVoltage()
        if volt < 11.2:
            print("Main battery:", volt)
            return True
    return False


def is_powersupply_enough():
    if polaris.isBatteryBackup():
        volt = polaris.readBattVoltage()
        if volt >= 3.6:
            return True
    else:
        volt = polaris.readMainVoltage()
        if volt >= 11.5:
            return True
    return False


def start():
    # only proceed if power supply input level is enough
    print("Checking power supply level...")
    while not is_powersupply_enough():
        polaris.ledRedOff()
        # pwr.go_to_sleep(450, pwr.PWR_STOP)
        sleep(450)
        polaris.ledRedOn()
        sleep(50)
    print("Starting utility thread...")
    thread(run)
    
def run():
    sms_timer = 0
    while True:
        mcu_reset = False
        sleep(1000)
        sms_timer += 1
        # parse SMS commands
        try:
            if check_sms and modem and (sms_timer >= 15 or modem.pending_sms() > 0):
                sms_timer = 0
                mcu_reset = read_and_parse_sms()
        except Exception as e:
            print("utils SMS failure", e)
        # control battery charger and input level
        if is_powersupply_toolow():
            print("Power supply too low!")
            mcu_reset = True
        else:
            update_charger()
        # handle reset
        if mcu_reset:
            if modem:
                modem.shutdown()
            print("utils MCU reset")
            mcu.reset()


def request_apn(s):
    apn = None
    while apn is None:
        print("Enter APN:")
        apn = input_line(s)
        if not validate_apn(apn):
            print("Invalid APN, try again!")
            apn = None
        if apn is not None and len(apn) == 0:
            print("Empty APN, confirm [y/n]")
            if input_line(s) == 'y':
                break
            else:
                apn = None
    return apn


def request_email(s):
    email = None
    while email is None:
        print("Enter email:")
        email = input_line(s)
        if not validate_email(email):
            print("Invalid email, try again!")
            email = None
    return email

led_state = False
led_count = 0


def status_led(sending, ignition, connected):
    global led_state, led_count
    if sending:
        led_state = False
        led_count = 0
        if ignition:
            polaris.ledRedOff()
            polaris.ledGreenOff()
        else:
            polaris.ledRedOn()
            polaris.ledGreenOn()
    else:
        if connected:
            if ignition:
                polaris.ledRedOff()
                polaris.ledGreenOn()
            else:
                polaris.ledRedOff()
                polaris.ledGreenOff()
        else:
            led_count += 1
            if led_count > 5:
                led_state = not led_state
                led_count = 0
            if led_state:
                polaris.ledRedOn()
            else:
                polaris.ledRedOff()
            polaris.ledGreenOff()
