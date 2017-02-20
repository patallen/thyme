"""
thyme

Usage:
  thyme random (<randthing>) [<limit>]
  thyme stamp <datestring>
  thyme date <timestamp> [--format=<fmt>]
  thyme --version
  thyme -h | --help

Options:
  -h --help
  --version                     Show Thyme version.

Examples:
    thyme random uuid         =>  63831617-f5b3-41bb-b2ce-94fb31719293
    thyme random int 100      =>  68
    thyme random float 1000   =>  999.9999999999999
    thyme random prime 100    =>  17
    thyme random secret 32    =>  fx%e!@%m7t!\%o/~u}v9)2N7e&gvG{%c
    thyme stamp 02-25-1990    =>  635922000
    thyme date 635922000      =>  02-25-1990
"""
from docopt import docopt
from .thyme import Thyme


def main():
    arguments = docopt(__doc__)
    thyme = Thyme(arguments)
    thyme.run()


if __name__ == '__main__':
    main()
