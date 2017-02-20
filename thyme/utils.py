import dateparser
from datetime import datetime
import arrow


def datetime_to_string(date, fmt):
    """Convert a datetime object to a string using provided format."""
    if not _validate_format(fmt):
        raise ValueError("Invalid format supplied.")
    fmt = fmt.upper()
    arrow_date = arrow.get(date)
    formatted = arrow_date.format(fmt)
    return formatted


def assert_all_equal(alist):
    """Assert that all objects in a list are equal."""
    last = alist[0]

    if len(alist) == 1:
        return True

    for l in alist:
        if l != last:
            return False
        last = l

    return True


def string_to_datetime(string):
    """Parse a date string and convert to datetime object."""
    parsed = dateparser.parse(string)
    if not parsed:
        raise ValueError("Could not parse date string.")
    return parsed


def make_timestamp(dt):
    """Turn a datetime object in to a Unix timestamp (UTC)."""
    try:
        timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    except TypeError:
        raise TypeError("Must provide a valid datetime object.")

    return int(timestamp)


def _validate_format(fmt):
    accept = 'YMD ,-/'
    return all([c in accept for c in fmt.upper()])
