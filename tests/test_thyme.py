from thyme.thyme import Thyme
from thyme.modes import DatetimeMode, TimestampMode


from thyme.cli import parser


def test_thyme_init():
    argv = 'date 12345656'.split()
    dt = Thyme(parser.parse_args(argv))
    assert dt._kwargs


def test_thyme__get_mode():
    argv = 'date 12345656'.split()
    dt = Thyme(parser.parse_args(argv))
    assert dt._get_mode(dt._kwargs) == DatetimeMode

    argv = ['stamp', '10-10-2010']
    stamp = Thyme(parser.parse_args(argv))
    assert stamp._get_mode(stamp._kwargs) == TimestampMode


def test_thyme_run():
    argv = 'date 12345656'.split()
    dt = Thyme(parser.parse_args(argv))
    assert dt.run() is None
