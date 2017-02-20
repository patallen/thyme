from datetime import datetime
import math
import random
import uuid
import string

import arrow
import dateparser


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


def gen_random_thing(randthing, limit=None):
    """Given a type string to match on, we generate a random instance.

    :param randthing: <str> Random thing we will generate.
    :param limit: <int> Size / max where applicable
    """
    randthing = randthing.lower()
    limit = limit or 100
    if randthing in ('uuid', 'guid', 'uid', 'uuid4'):
        return uuid.uuid4()
    if randthing in ('int', 'integer', 'num', 'number'):
        return _random_int(limit)
    if randthing in ('float', 'decimal', 'dec'):
        return _random_float(limit)
    if randthing in ('secret', 'secret_key', 'hash'):
        return _random_secret(limit)

    raise ValueError("Not a valid random thing.")


def _random_secret(length=64):
    chars = string.printable
    return "".join([chars[_random_int(len(chars))] for _ in range(length)])


def _random_int(upper_bound):
    rand = random.random()
    return int(math.floor(rand * (upper_bound + 1)))


def _random_float(upper_bound):
    return random.random() * upper_bound


def _validate_format(fmt):
    accept = 'YMD ,-/'
    return all([c in accept for c in fmt.upper()])
