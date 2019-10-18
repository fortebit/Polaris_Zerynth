import json
import mcu
import sfw
import timers
from fortebit.polaris import polaris

has_qspi = True


def decimal(n, v):
    v = float(v)
    s = "%%.%df" % n
    s = s % v
    if len(str(v)) < len(s):
        return s[:-1] + '0'
    return s

gsm = ("@\t$\t\t\t\t\t\t\t\n\t\t\r\t\t\t_\t\t\t\t\t\t\t\t\t\x1b\t\t\t\t !\"# %&'()*+,-./0123456789:;<=>?"
       " ABCDEFGHIJKLMNOPQRSTUVWXYZ    ` abcdefghijklmnopqrstuvwxyz     ")
ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
       "|```````````````````````````````````` ``````````````````````````")


def gsm_encode(plaintext):
    result = []
    for c in plaintext:
        idx = gsm.find(c)
        if idx != -1:
            result.append(chr(idx))
            continue
        idx = ext.find(c)
        if idx != -1:
            result.append(chr(27) + chr(idx))
    return ''.join(result)


def gsm_decode(res):
    result = []
    i = 0
    while i < len(res):
        c = res[i]
        i += 1
        if c == chr(27):
            c = res[i]
            i += 1
            result.append(ext[ord(c)])
        else:
            result.append(gsm[ord(c)])
    return ''.join(result)


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


def readSMS(gsm):
    while True:
        sms = gsm.list_sms()
        mcu_reset = False
        if sms and len(sms) > 0:
            mcu_reset = False
            for msg in sms:
                print("Index:", msg[3])
                print("Text:", msg[0])
                print("From:", msg[1])
                print("Time:", msg[2])
                gsm.delete_sms(msg[3])
                text = gsm_decode(msg[0])
                text = text.split(",")
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
                    gsm.send_sms(msg[1], gsm_encode(ret))
        sleep(5000)
        if mcu_reset:
            print("mcu reset")
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
