import argparse
from . import modes


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
random_float.add_argument('-l', '--limit', dest='limit')
random_float.add_argument('limit')


random_int = random_subparsers.add_parser(
    'int',
    help='Generate a random integer.'
)
random_int.add_argument('-l', '--limit', dest='limit')
random_int.add_argument('limit')


random_secret = random_subparsers.add_parser(
    'secret',
    help='Generate a random ASCII secret key.'
)
random_secret.add_argument('-l', '--limit', dest='limit')
random_secret.add_argument('limit')


def dispatch_mode(args):
    command = args.command
    if command == 'random':
        res = modes.RandomMode(args)
    elif command == 'date':
        res = modes.DatetimeMode(args)
    elif command == 'stamp':
        res = modes.TimestampMode(args)
    else:
        raise Exception("Some error.")

    return res.execute()


def main():
    args = parser.parse_args()
    res = dispatch_mode(args)
    print(res)

if __name__ == '__main__':
    main()
