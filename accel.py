import threading
import math
from fortebit.polaris import accelerometer as accel

_lock = threading.Lock()
_accel = accel.Accelerometer()
_thread = None

_ACCEL_LP_COEF = 0.25
_ACCEL_UPDATE = 10
_x = 0.0
_y = 0.0
_z = 0.0
_peak = 0.0

_alive = 0
_except = 0

def _update():
    _lock.acquire()
    try:
        global _x,_y,_z,_peak
        a = _accel.acceleration()
        _x = _ACCEL_LP_COEF * a[0] + (1-_ACCEL_LP_COEF) * _x
        _y = _ACCEL_LP_COEF * a[1] + (1-_ACCEL_LP_COEF) * _y
        _z = _ACCEL_LP_COEF * a[2] + (1-_ACCEL_LP_COEF) * _z
        #print("inc: ",_x,_y,_z,a)
        # update peak diff
        d_x = a[0] - _x
        d_y = a[1] - _y
        d_z = a[2] - _z
        d2 = d_x*d_x + d_y*d_y + d_z*d_z
        if d2 > _peak:
            _peak = d2
    except Exception as e:
        pass
    _lock.release()

def _run(arg):
    global _alive, _except
    # discard initial samples (accel filters need time to stabilize)
    _lock.acquire()
    try:
        for n in range(15):
            sleep(10)
            _accel.acceleration()
        _peak = 0.0
    except Exception as e:
        pass
    _lock.release()
    # refresh
    while True:
        try:
            _update()
        except Exception as e:
            print("Accel task:",e)
            _except = _except + 1
        sleep(_ACCEL_UPDATE)
        _alive = _alive + 1
    
def get_pitchroll():
    _lock.acquire()
    tmp = math.sqrt(_y*_y + _z*_z);
    pitch = math.degrees(math.atan2(-_x, tmp))
    roll = math.degrees(math.atan2(_y, _z))
    _lock.release()
    return (pitch, roll)

def get_temperature():
    _lock.acquire()
    t = _accel.temperature()
    _lock.release()
    return t

def get_sigma():
    _lock.acquire()
    sigma = math.sqrt(_peak)
    _peak = 0.0
    _lock.release()
    return sigma
    
def start():
    _lock.acquire()
    try:
        if _thread is None:
            _thread = thread(_run,"Accel Task")
        global _x,_y,_z
        (_x,_y,_z) = _accel.acceleration()
    except Exception as e:
        pass
    _lock.release()
