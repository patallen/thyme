"""CLI Interface for Thyme"""

import argparse
from .thyme import Thyme


parser = argparse.ArgumentParser(
    prog='Thyme',
    description='Developer\'s Convenience CLI',
)

subparsers = parser.add_subparsers(
    dest='command',
    help='Choose wisely...'
)
subparsers.required = True

random = subparsers.add_parser(
    'random',
    help='Generate a random integer, float, UUID or secret key.'
)

file = subparsers.add_parser(
    'file',
    help='Create a file based off of a basic template.'
)
file_subparsers = file.add_subparsers(dest="filetype")
file_subl = file_subparsers.add_parser(
    'subl', help="Generate a sublime-project file.")
file_subl.add_argument(
    '--name', '-n', dest='name',
    help='Choose a name. (defaults to cwd)')

# file.add_argument()
date = subparsers.add_parser(
    'date',
    help='Convert a Unix timestamp to a UTC datetime.'
)
date.add_argument('timestamp')
date.add_argument('-f', '--format', dest='format')

stamp = subparsers.add_parser(
    'stamp',
    help='Convert a UTC datetime to a Unix timestamp.'
)
stamp.add_argument('date')

convert = subparsers.add_parser(
    'convert',
    help='Convert something to something else.'
)
convert.add_argument('toconvert')


random_subparsers = random.add_subparsers(
    dest='type',
    help='Generate something random for development purposes.',
)
random_subparsers.required = True

random_sub = random_subparsers.add_parser(
    'uuid',
    help='Generate a UUID'
)

random_float = random_subparsers.add_parser(
    'float',
    help='Generate a random floating point integer.'
)
random_float.add_argument('-l', '--limit', dest='limit', default=100)


random_int = random_subparsers.add_parser(
    'int',
    help='Generate a random integer.'
)
random_int.add_argument('-l', '--limit', dest='limit', default=100)


random_secret = random_subparsers.add_parser(
    'secret',
    help='Generate a random ASCII secret key.'
)
random_secret.add_argument('-l', '--limit', dest='limit', default=64)


history = subparsers.add_parser(
    'history',
    help='Thyme History'
)
history.add_argument('search', default=None, nargs='?')


def main():
    args = parser.parse_args()
    thyme = Thyme(args)
    thyme.run()

if __name__ == '__main__':
    main()
