"""
.. module:: polaris

**************
Polaris Module
**************

This module provides easy access to the Polaris board features, meaningful names
for MCU pins and peripherals, simplified initialization of on-board devices.

    """

# Main Connector
class main:
    """
.. class:: main

    Namespace for the **Main** connector signals and related peripherals:
    
    * ``PIN_VIN`` - analog input for main supply voltage
    * ``PIN_IGNITION`` - digital input for ignition detection (active high)
    * ``PIN_SOS`` - digital input for emergency button (active low)
    * ``PIN_AIN1``, ``PIN_RANGE_IN1`` - analog input 1 and range selection pin
    * ``PIN_AIN2``, ``PIN_RANGE_IN2`` - analog input 2 and range selection pin
    * ``PIN_AIN3``, ``PIN_RANGE_IN3`` - analog input 3 and range selection pin
    * ``PIN_AIN4``, ``PIN_RANGE_IN4`` - analog input 4 and range selection pin
    * ``PIN_IOEXP_IN1`` - control input 1 for I/O Expander
    * ``PIN_IOEXP_IN2`` - control input 2 for I/O Expander
    
    * ``ADC_VIN`` - ADC channel (using ``PIN_VIN``)
    * ``ADC_IN1`` - ADC channel (using ``PIN_AIN1``)
    * ``ADC_IN2`` - ADC channel (using ``PIN_AIN2``)
    * ``ADC_IN3`` - ADC channel (using ``PIN_AIN3``)
    * ``ADC_IN4`` - ADC channel (using ``PIN_AIN4``)
    * ``PWM_IOEXP_IN1`` - PWM control input 1 for I/O Expander
    * ``PWM_IOEXP_IN2`` - PWM control input 2 for I/O Expander
    """
    PIN_VIN = D20

    PIN_IGNITION = D44
    PIN_SOS = D71

    PIN_AIN1 = D21
    PIN_AIN2 = D23
    PIN_AIN3 = D41
    PIN_AIN4 = D42

    PIN_RANGE_IN4 = D62
    PIN_RANGE_IN3 = D64
    PIN_RANGE_IN2 = D72
    PIN_RANGE_IN1 = D73

    PIN_IOEXP_IN1 = D22
    PIN_IOEXP_IN2 = D65

    ADC_VIN = A4
    ADC_IN1 = A5
    ADC_IN2 = A6
    ADC_IN3 = A7
    ADC_IN4 = A8

    PWM_IOEXP_IN1 = PWM13
    PWM_IOEXP_IN2 = PWM14

# MikroBus
class mikrobus:
    """
.. class:: mikrobus

    Namespace for the **mikroBUS** expansion interface signals and related peripherals:
    
    * ``PIN_MISO``, ``PIN_MOSI``, ``PIN_SCK``, ``PIN_CS`` - expansion SPI interface
    * ``PIN_SDA``, ``PIN_SCL`` - expansion I2C interface
    * ``PIN_TX``, ``PIN_RX`` - expansion UART pins
    * ``PIN_RST``, ``PIN_INT`` - general purpose I/O pins (usually reset and interrupt) 
    * ``PIN_PWM`` - PWM capable pin
    * ``PIN_AN`` - analog input pin
    
    * ``SERIAL`` - serial driver (using ``PIN_RX``,``PIN_TX``)
    * ``SPI`` - SPI driver (using ``PIN_MISO``, ``PIN_MOSI``, ``PIN_SCK``)
    * ``I2C`` - I2C driver (using ``PIN_SDA``, ``PIN_SCL``)
    * ``PWM`` - PWM channel (using ``PIN_PWM``)
    * ``ADC`` - ADC channel (using ``PIN_AN``)
    """
    PIN_AN = D0
    PIN_RST = D1
    PIN_CS = D2
    PIN_SCK = D3
    PIN_MISO = D4
    PIN_MOSI = D5
    PIN_PWM = D6
    PIN_INT = D7
    PIN_RX = D8
    PIN_TX = D9
    PIN_SCL = D10
    PIN_SDA = D11

    SERIAL = SERIAL1
    SPI = SPI0
    I2C = I2C0
    PWM = PWM2
    ADC = A0

# ExtBus
class extbus:
    """
.. class:: extbus

    Namespace for the **Ext-A** expansion interface signals and related peripherals:
    
    * ``PIN_GPIO1``, ``PIN_GPIO2`` - general purpose I/O pins
    * ``PIN_TX``, ``PIN_RX`` - expansion UART pins
    * ``PIN_PWM`` - PWM capable pin
    * ``PIN_AN1`` - analog input pin
    * ``PIN_DAC1``, ``PIN_DAC1`` - analog pins
    
    * ``SERIAL`` - serial driver (using ``PIN_RX``,``PIN_TX``)
    * ``PWM`` - PWM channel (using ``PIN_PWM``)
    * ``ADC`` - ADC channel (using ``PIN_AN1``)
    """
    PIN_GPIO1 = D12
    PIN_GPIO2 = D13
    PIN_TX = D14
    PIN_RX = D15
    PIN_PWM = D16
    PIN_AN1 = D17
    PIN_DAC2 = D18
    PIN_DAC1 = D19

    SERIAL = SERIAL2
    PWM = PWM5
    ADC = A1

# Internal signals
class internal:
    """
.. class:: internal

    Namespace for on-board devices signals and peripherals:
    
    * ``PIN_LED_RED``, ``PIN_LED_GREEN`` - LED control pins (active low)
    * ``PIN_POWER_DIS`` - main power control pin (shutdown)
    * ``PIN_5V_EN`` - control pin for 5V regulator
    * ``PIN_BATT_EN`` - backup battery status pin
    * ``PIN_IOEXP_CS`` - I/O Expander chip-select pin
    * ``PIN_ACCEL_CS``, ``PIN_ACCEL_INT`` - accelerometer chip-select and interrupt pins
    * ``PIN_CHARGE_PROG``, ``PIN_CHARGE_STAT`` - backup battery charger control and status pins
    * ``PIN_BATT_ADC`` - analog input for backup battery voltage
    
    * ``SPI`` - on-board SPI driver (for accelerometer and I/O Expander)
    * ``ADC_BATT`` - ADC channel (using ``PIN_BATT_ADC``)
    """
    PIN_LED_RED = D35
    PIN_LED_GREEN = D63
    
    PIN_POWER_DIS = D51
    PIN_BATT_EN = D69
    PIN_5V_EN = D70

    PIN_CHARGE_PROG = D26
    PIN_CHARGE_STAT = D56
    PIN_BATT_ADC = D43

    PIN_ACCEL_CS = D60
    PIN_ACCEL_INT = D61

    PIN_IOEXP_CS = D76

    SPI = SPI1
    PWM_CHARGE = PWM9
    ADC_BATT = A9

# Signals used for global positioning module
class gnss:
    """
.. class:: gnss

    Namespace for GNSS module signals and related peripherals:
    
    * ``PIN_STANDBY``, ``PIN_RESET`` - module control pins
    * ``PIN_TX``, ``PIN_RX`` - module UART pins
    * ``PIN_ANTON`` - control pin (used only in the NB-IoT variant with BG96)
    
    * ``SERIAL`` - serial driver (using ``PIN_RX``,``PIN_TX``)
    """
    PIN_STANDBY = D45
    PIN_RESET = D59
    PIN_TX = D27
    PIN_RX = D28
    PIN_ANTON = D80

    SERIAL = SERIAL4

# Signals used for GSM module
class gsm:
    """
.. class:: gsm

    Namespace for Modem signals and related peripherals:
    
    * ``PIN_TX``, ``PIN_RX`` - modem UART pins
    * ``PIN_POWER``, ``PIN_KILL``, ``PIN_WAKE`` - modem control pins
    * ``PIN_STATUS``, ``PIN_RING`` - modem status pins
    
    * ``SERIAL`` - serial driver (using ``PIN_RX``,``PIN_TX``)
    """
    PIN_TX = D57
    PIN_RX = D58
    PIN_STATUS = D37
    PIN_POWER = D67
    PIN_WAKE = D68
    PIN_KILL = D38
    PIN_RING = D54

    SERIAL = SERIAL3

# Public globals
CHARGE_NONE = 0
CHARGE_BUSY = 1
CHARGE_COMPLETE = 2
IGNITION_OFF = 0
IGNITION_ON = 1
SOS_OFF = 0
SOS_ON = 1

# Private globals
_PIN_NC = -1
_ANALOG_VREF = 2.50
_ANALOG_SCALE = 13.0154525
_ANALOG_SCALE_LOW = 2.0
_ADC2VOLT = _ANALOG_VREF * _ANALOG_SCALE / 4095
_ADC2VOLT_LOW = _ANALOG_VREF * _ANALOG_SCALE_LOW / 4095

# Default initialization
import streams
streams.serial(SERIAL0)
import adc

def init():
    """
.. function:: init()

    Performs required initializion of Polaris pins and common functionalities.
    It should be called at the start of your application.
    """
    # Setup power
    digitalWrite(internal.PIN_POWER_DIS, LOW)
    pinMode(internal.PIN_POWER_DIS, OUTPUT)
    digitalWrite(internal.PIN_POWER_DIS, LOW)
    pinMode(internal.PIN_BATT_EN, INPUT)
    pinMode(internal.PIN_5V_EN, OUTPUT)
    digitalWrite(internal.PIN_5V_EN, HIGH)
    pinMode(internal.PIN_CHARGE_STAT, INPUT)
    pinMode(main.PIN_IGNITION, INPUT)
    pinMode(main.PIN_SOS, INPUT)
    pinMode(internal.PIN_CHARGE_PROG, OUTPUT)
    digitalWrite(internal.PIN_CHARGE_PROG, HIGH)
    # reboot on power supply input changes
    if digitalRead(internal.PIN_BATT_EN) == LOW:
        onPinRise(internal.PIN_BATT_EN, shutdown)
    else:
        onPinFall(internal.PIN_BATT_EN, shutdown)

def isBatteryBackup():
    """
.. function:: isBatteryBackup()

    Returns a boolean value to indicate whether the board is powered from the backup battery source.
    """
    pinMode(internal.PIN_BATT_EN, INPUT)
    return True if digitalRead(internal.PIN_BATT_EN) == HIGH else False

def setBatteryCharger(enable):
    """
.. function:: setBatteryCharger(enable)

    Enables or disables the backup battery charger (5V required).
    
    :note: Do not enable the charger when the main power supply is not present
    """
    pinMode(internal.PIN_CHARGE_PROG, OUTPUT)
    digitalWrite(internal.PIN_CHARGE_PROG, LOW if enable else HIGH)

def getChargerStatus():
    """
.. function:: getChargerStatus()

    Returns the battery charger status (not charging, charging or fully charged).
    
    :returns: One of these values: ``CHARGE_NONE`` = 0, ``CHARGE_BUSY`` = 1, ``CHARGE_COMPLETE`` = 2
    """
    pinMode(internal.PIN_CHARGE_STAT, INPUT_PULLDOWN)
    res = 1 if digitalRead(internal.PIN_CHARGE_STAT) == HIGH else 0
    pinMode(internal.PIN_CHARGE_STAT, INPUT_PULLUP)
    res = (res << 1) + (1 if digitalRead(internal.PIN_CHARGE_STAT) == HIGH else 0)
    if res == 0:
        return CHARGE_BUSY
    if res == 3:
        return CHARGE_COMPLETE
    return CHARGE_NONE

def getIgnitionStatus():
    """
.. function:: getIgnitionStatus()

    Reads the ignition status from digital input pin IGN/DIO5 (active high).
    
    :returns: An integer value to indicate whether the ignition switch is on/off: ``IGNITION_ON`` = 1 or ``IGNITION_OFF`` = 0
    """
    pinMode(main.PIN_IGNITION, INPUT_PULLUP)
    if digitalRead(main.PIN_IGNITION) == LOW:
        return IGNITION_ON
    else:
        return IGNITION_OFF

def getEmergencyStatus():
    """
.. function:: getEmergencyStatus()

    Reads the emergency button status from digital input pin SOS/DIO6 (active low).
    
    :returns: An integer value to indicate whether the emergency button is switched on/off: ``SOS_ON`` = 1 or ``SOS_OFF`` = 0
    """
    pinMode(main.PIN_SOS, INPUT_PULLDOWN)
    if digitalRead(main.PIN_SOS) == HIGH:
        return SOS_ON
    else:
        return SOS_OFF

def shutdown():
    """
.. function:: shutdown()

    Disables the main regulator or backup battery source, effectively power-cycling the board.
    """
    pinMode(internal.PIN_POWER_DIS, OUTPUT)
    digitalWrite(internal.PIN_POWER_DIS, HIGH)

def GSM():
    """
.. function:: GSM()

    Initializes the correct Modem library for the Polaris board variant and
    returns the module object.
    
    :returns: ``UG96`` for *Polaris 3G*, ``M95`` for *Polaris 2G* (*Polaris NB-IoT* not supported yet)
    """
    #-if TARGET == polaris_3g
    from quectel.ug96 import ug96
    ug96.init(gsm.SERIAL, _PIN_NC, _PIN_NC, gsm.PIN_POWER, gsm.PIN_KILL, gsm.PIN_STATUS, 1, 1, 0)
    return ug96
    #-else 
    ##-if TARGET == polaris_2g
    from quectel.m95 import m95
    m95.init(gsm.SERIAL, _PIN_NC, _PIN_NC, gsm.PIN_POWER, gsm.PIN_KILL, gsm.PIN_STATUS, 1, 1, 0)
    return m95
    ##-else
    ###-if TARGET == polaris_nbiot
    from quectel.bg96 import bg96
    bg96.init(gsm.SERIAL, _PIN_NC, _PIN_NC, gsm.PIN_POWER, gsm.PIN_KILL, gsm.PIN_STATUS, 1, 1, 0)
    bg96.gnss_init(use_uart=1)
    return bg96
    ###-else
    raise UnsupportedError
    ###-endif
    ##-endif
    #-endif

def GNSS():
    """
.. function:: GNSS()

    Creates an instance of the correct GNSS receiver class for the Polaris board variant.
    
    :returns: ``L76`` for *Polaris 3G* and *Polaris 2G* (*Polaris NB-IoT* not supported yet)
    """
    #-if TARGET == polaris_3g
    from quectel.l76 import l76
    l = l76.L76(gnss.SERIAL)
    l.start(gnss.PIN_RESET)
    return l
    #-else
    ##-if TARGET == polaris_2g
    from quectel.l76 import l76
    l = l76.L76(gnss.SERIAL)
    l.start(gnss.PIN_RESET)
    return l
    ##-else
    ###-if TARGET == polaris_nbiot
    from quectel.l76 import l76
    l = l76.L76(gnss.SERIAL,baud=115200)
    pinMode(gnss.PIN_ANTON, OUTPUT)
    digitalWrite(gnss.PIN_ANTON, HIGH)
    l.start()
    return l
    ###-else
    raise UnsupportedError
    ###-endif
    ##-endif
    #-endif

def QSpiFlash():
    """
.. function:: QSpiFlash()

    Creates an instance of the on-board Quad-Spi Flash device class.
    
    :returns: ``QSpiFlash`` object configured for Polaris hardware
    """
    import qspiflash
    return qspiflash.QSpiFlash(D34,D33,D25,D24,D74,D75,0x100000,0x10000,0x8000,0x1000,0x100,8,4,4,2,4,0xA5,0x00,0x01,0x02,0x7C,0x80,0x02,0x80)

def IOExpander():
    """
.. function:: IOExpander()

    Creates an instance of the on-board I/O Expander device class (``NCV7240``).
    
    :returns: ``QSpiFlash`` object configured for Polaris hardware
    """
    from onsemi.ncv7240 import ncv7240
    return ncv7240.NCV7240(internal.SPI, internal.PIN_IOEXP_CS)

def Accelerometer():
    """
.. function:: Accelerometer()

    Creates an instance of the on-board accelerometer device class (``LIS2HH12``).
    
    :returns: ``QSpiFlash`` object configured for Polaris hardware
    """
    from stm.lis2hh12 import lis2hh12
    return lis2hh12.LIS2HH12(internal.SPI, internal.PIN_ACCEL_CS)

def readMainVoltage():
    """
.. function:: readMainVoltage()

    Returns the analog measure of the main supply voltage.
    """
    pinMode(main.PIN_VIN, INPUT_ANALOG)
    return 0.25 + analogRead(main.ADC_VIN) * _ADC2VOLT

def readBattVoltage():
    """
.. function:: readMainVoltage()

    Returns the analog measure of the backup battery voltage.
    """
    pinMode(internal.PIN_BATT_ADC, INPUT_ANALOG)
    return analogRead(internal.ADC_BATT) * _ADC2VOLT_LOW

_AIN_ARRAY = (
    (main.ADC_IN1, main.PIN_RANGE_IN1),
    (main.ADC_IN2, main.PIN_RANGE_IN2),
    (main.ADC_IN3, main.PIN_RANGE_IN3),
    (main.ADC_IN4, main.PIN_RANGE_IN4),
)

def readAnalogInputVoltage(pin_num, range=HIGH):
    """
.. function:: readAnalogInputVoltage(pin_num, range=HIGH)

    Returns the voltage measure of an analog input pin on the **Main** connector.
    
    :param pin_num: Index of the analog pin (0-3 = corresponds to AIO1-4)
    :param range: Full-scale range: *HIGH* (0-36V) or *LOW* (0-5V)
    """
    pinMode(_AIN_ARRAY[pin_num][0], INPUT_ANALOG)
    pinMode(_AIN_ARRAY[pin_num][1], OUTPUT)
    digitalWrite(_AIN_ARRAY[pin_num][1], range)
    a = analogRead(_AIN_ARRAY[pin_num][0])
    if range == HIGH:
        return a * _ADC2VOLT
    return a * _ADC2VOLT_LOW

def ledRedOff():
    """
.. function:: ledRedOff()

    Switch the red LED off.
    """
    pinMode(internal.PIN_LED_RED, OUTPUT)
    digitalWrite(internal.PIN_LED_RED, HIGH)

def ledRedOn():
    """
.. function:: ledRedOn()

    Switch the red LED on.
    """
    pinMode(internal.PIN_LED_RED, OUTPUT)
    digitalWrite(internal.PIN_LED_RED, LOW)

def ledGreenOff():
    """
.. function:: ledGreenOff()

    Switch the green LED off.
    """
    pinMode(internal.PIN_LED_GREEN, OUTPUT)
    digitalWrite(internal.PIN_LED_GREEN, HIGH)

def ledGreenOn():
    """
.. function:: ledGreenOn()

    Switch the green LED on.
    """
    pinMode(internal.PIN_LED_GREEN, OUTPUT)
    digitalWrite(internal.PIN_LED_GREEN, LOW)
