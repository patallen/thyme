import pytest


from thyme.modes import TimestampMode
from thyme.results import ValidResult, InvalidResult


from thyme.cli import parser


return_stamp = 635904000


def test_timestamp_mode_good_kwargs():
    argv = ['stamp', 'feb 25 1990']
    args = parser.parse_args(argv)
    timestamp_mode = TimestampMode(args)

    assert isinstance(timestamp_mode.execute(), ValidResult)

    assert timestamp_mode.execute().result == return_stamp


def test_timestamp_mode_bad_kwargs():
    argv = 'stamp 34kjk3j4523k'.split()
    args = parser.parse_args(argv)

    timestamp_mode = TimestampMode(args)

    assert isinstance(timestamp_mode.execute(), InvalidResult)


@pytest.mark.parametrize('args, expected', [
    (('stamp', '02/25/1990'), 'stamp 02/25/1990'),
    (('stamp', 'Feb 25, 1990'), "stamp 'Feb 25, 1990'")
])
def test_timestamp_str_representation(args, expected):
    parsed = parser.parse_args(args)
    timestamp_mode = TimestampMode(parsed)
    assert str(timestamp_mode) == expected
