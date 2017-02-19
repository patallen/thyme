import re


FORMAT_PARTS = {
    'yyyy': '%Y',
    'yy': '%y',
    'dd': '%d',
    'mm': '%m'
}


def convert_fmt(fmt):
    try:
        fmt = fmt.lower()
        delim = _find_delimiter(fmt)
        fmt_parts = fmt.split(delim)
    except ValueError:
        delim = ""
        fmt_parts = _find_parts(fmt)
    except AttributeError:
        return convert_fmt('mm/dd/yyyy')

    parts = []
    for f in fmt_parts:
        parts.append(FORMAT_PARTS[f])

    return delim.join(parts)


def _find_delimiter(format_):
    for c in format_:
        if not c.isalnum():
            return c

    raise ValueError

possible_parts = [('yyyy', 'yy'), ('mm',), ('dd',)]


def _find_parts(fmt):
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
