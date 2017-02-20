import re
import dateparser
from datetime import datetime

_FORMAT_PARTS = {
    'yyyy': '%Y',
    'yy': '%y',
    'dd': '%d',
    'mm': '%m'
}


def assert_all_equal(alist):
    last = alist[0]

    if len(last) == 1:
        return True

    for l in alist:
        if l != last:
            return False
        last = l

    return True


def get_strftime_format(fmt):
    fmt = fmt.lower()
    delim = _find_delimiter(fmt)
    parts = _find_parts(fmt, delim)
    strftime_fmt = _fmt_from_parts(parts, delim)
    return strftime_fmt


def _fmt_from_parts(parts, delimiter):
    fmt_parts = []
    for f in parts:
        fmt_parts.append(_FORMAT_PARTS[f])

    return delimiter.join(fmt_parts)


def _find_delimiter(format_):
    non_alphas = []
    for c in format_:
        if not c.isalnum():
            non_alphas.append(c)

    if assert_all_equal(non_alphas):
        return non_alphas[0]

    raise ValueError("Delimiters must all be the same.")

possible_parts = [('yyyy', 'yy'), ('mm',), ('dd',)]


def _find_parts(fmt, delimiter):
    if delimiter:
        return fmt.split(delimiter)

    if not delimiter:
        part_positions = []
        for poss in possible_parts:
            for p in poss:
                match = re.search(p, fmt)
                if match:
                    part_positions.append((p, match.start()))
                    break
    if not part_positions:
        return ['mm', 'dd', 'yyyy']

    part_positions.sort(key=lambda x: x[1])
    return [p[0] for p in part_positions]


def string_to_datetime(string):
    parsed = dateparser.parse(string)
    if not parsed:
        raise ValueError("Could not parse date string.")
    return parsed


def make_timestamp(dt):
    try:
        timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
    except TypeError:
        raise TypeError("Must provide a valid datetime object.")

    return int(timestamp)


__all__ = [
    get_strftime_format,
    assert_all_equal,
    string_to_datetime
]

