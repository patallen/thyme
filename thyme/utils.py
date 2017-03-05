import random


class DenomedSize(object):
    def __init__(self, value, byterate):
        self.byterate = byterate
        self.value = value

    @classmethod
    def from_string(cls, string):
        """Evaluate a size string and turn it into a DenomedSize instance."""
        value, denom = _parse_size_string(string)
        try:
            return cls(value, RATE_MAP[denom.lower()])
        except KeyError:
            raise ValueError(
                "'{}' is not a valid size denomination.".format(denom))

    def to_bytes(self):
        """Return the size converted into bytes."""
        return self.byterate * self.value


class ByteRate(object):
    """A simple helper object for encapsulating byte rate information."""

    def __init__(self, value, name, abbreviation):
        self.name = name
        self.value = value
        self.abbreviation = abbreviation

    def __mul__(self, other):
        return other * self.value

RATE_MAP = {
    'b': ByteRate(1, 'Bytes', 'b'),
    'kb': ByteRate(1024, 'Kilobytes', 'kb'),
    'mb': ByteRate(1048576, 'Megabytes', 'mb'),
    'gb': ByteRate(1073741824, 'Gigabytes', 'gb'),
    'tb': ByteRate(1099511627776, 'Terabytes', 'tb'),
    'pb': ByteRate(1125899906842624, 'Petabytes', 'pb'),
}


def _parse_size_string(string):
    for index, char in enumerate(str(string)):
        if char not in '1234567890':
            return (int(string[:index]), string[index:])
    raise ValueError("Size string requires digits and letters.")


def get_all_rates(bytes_):
    """Convert bytes to kb, mb, gb, tb, and pb."""
    converteds = [(bytes_ / v.value, k) for k, v in RATE_MAP.items()]
    return sorted(converteds, key=lambda x: x[0], reverse=True)


def format_rates(rates):
    """Return the rates formatted in a visually appealing way."""
    indent = max([len(r.name) for r in RATE_MAP.values()])

    def _pad_name(name):
        padding = " " * (indent - len(name))
        return "{0}{1}:  ".format(padding, name)

    tups = [(_pad_name(RATE_MAP[r[1]].name), r[0]) for r in rates]
    formatted = ("{}{:g}".format(*tup) for tup in tups)
    return "\n".join(formatted)


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
    """Assert that all objects in a list are equal.

    Returns True if len(alist) <= 1. Else, check them.
    """
    try:
        val = alist[1]
    except IndexError:
        return True
    return all(a == val for a in alist)


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


def gen_random_thing(randthing, limit=100):
    """Given a type string to match on, we generate a random instance.

    :param randthing: <str> Random thing we will generate.
    :param limit: <int> Size / max where applicable
    """
    options = {
        'uuid': random_uuid,
        'int': random_int,
        'float': random_float,
        'secret': random_secret,
    }
    return options[randthing.lower()](limit)


def random_secret(length=64):
    """Generate a secret of the specified length.

    Randomized from a list of most ASCII printable characters.
    >>> len(random_secret(100))
    100
    """
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    digits = '0123456789'
    chars = '!@#$%^&*()?~-_=+:;,.`'
    cs = '{0}{1}{2}{3}'.format(lower, upper, digits, chars)
    thing = "".join(cs[random_int(len(cs) - 1)] for _ in range(length))
    return thing.format('hex')


def random_uuid(unused_param=None):
    """Return a random UUID (uuid.uuid4).

    This takes an unused param so that we can use a dict in gen_random_thing.
    """
    import uuid
    return uuid.uuid4()


def random_int(upper_bound):
    """Generate a random integer inclusive of 0 and the upper_bound."""
    result = random.randint(0, upper_bound)
    return result


def random_float(upper_bound):
    """Generate a random float inclusive of 0 and the upper_bound."""
    return random.random() * upper_bound


def _validate_format(fmt):
    accept = 'YMD ,-/'
    return all(c in accept for c in fmt.upper())
