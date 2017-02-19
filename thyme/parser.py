import argparse

parser = argparse.ArgumentParser(prog='Thyme', description='Commandline datetime utility.')
parser.add_argument('datething')


parser.mutu
parser.add_argument('-ts', '--timestamp', type=float, help="From timestamp")
parser.add_argument('-f', '--format', type=str, help="From timestamp")

parser.add_argument('-d', '--datetime', '--date', type=str, help="Timestamp from date.")


args = parser.parse_args()
