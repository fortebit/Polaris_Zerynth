# Utility functions, adapted from Python's Demo/classes/Dates.py, which
# also assumes the current Gregorian calendar indefinitely extended in
# both directions.  Difference:  Dates.py calls January 1 of year 0 day
# number 1.  The code here calls January 1 of year 1 day number 1.  This is
# to match the definition of the "proleptic Gregorian" calendar in Dershowitz
# and Reingold's "Calendrical Calculations", where it's the base calendar
# for all computations.  See the book for algorithms for converting between
# proleptic Gregorian ordinals and many other calendar systems.

# -1 is a placeholder for indexing purposes.
_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
#del dbm, dim

def _is_leap(year):
    """year -> 1 if leap year, else 0."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _days_before_year(year):
    """year -> number of days before January 1st of year."""
    y = year - 1
    return y*365 + y//4 - y//100 + y//400

def _days_in_month(year, month):
    """year, month -> number of days in that month in that year."""
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]

def _days_before_month(year, month):
    """year, month -> number of days in year preceding first day of month."""
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))

def _ymd2ord(year, month, day):
    """year, month, day -> ordinal, considering 01-Jan-0001 as day 1."""
    dim = _days_in_month(year, month)
    return (_days_before_year(year) + _days_before_month(year, month) + day)

_EPOCH_START = _ymd2ord(1970,1,1)

def to_unix(ts):
    """Converts a date/time tuple to Unix timestamp in seconds"""
    return (((_ymd2ord(ts[0],ts[1],ts[2])-_EPOCH_START)*24+ts[3])*60+ts[4])*60+ts[5]
