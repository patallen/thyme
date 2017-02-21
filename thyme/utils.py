
def datetime_to_string(date, fmt):
    """Convert a datetime object to a string using provided format."""
    import arrow
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
    from datetime import datetime
    from dateutil.parser import parse

    parsed = parse(string, default=datetime(1, 1, 1))

    return parsed


def make_timestamp(dt):
    """Turn a datetime object in to a Unix timestamp (UTC)."""
    from datetime import datetime
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
    import uuid as uu
    randthing = randthing.lower()
    limit = limit or 100
    if randthing == 'uuid':
        return uu.uuid4()
    if randthing in 'int':
        return _random_int(limit)
    if randthing in 'float':
        return _random_float(limit)
    if randthing in 'secret':
        return _random_secret(limit)

    raise ValueError("Not a valid random thing.")


def _random_secret(length=64):
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    digits = '0123456789'
    chars = '!@#$%^&*()?~-_=+:;,.`'
    cs = '%s%s%s%s' % (lower, upper, digits, chars)
    thing = "".join([cs[_random_int(len(cs) - 1)] for _ in range(length)])
    return thing.format('hex')


def _random_int(upper_bound):
    import math
    import random
    rand = random.random()
    return int(math.floor(rand * (upper_bound + 1)))


def _random_float(upper_bound):
    import random
    return random.random() * upper_bound


def _validate_format(fmt):
    accept = 'YMD ,-/'
    return all([c in accept for c in fmt.upper()])
