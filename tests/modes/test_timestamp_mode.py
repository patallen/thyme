from thyme.modes import TimestampMode
from thyme.results import ValidResult, InvalidResult


from thyme.cli import parser


date_string = 'feb 25 1990'
return_stamp = 635904000


def test_timestamp_mode_good_kwargs():
    argv = ['date', 'feb 25 1990']
    args = parser.parse_args(argv)
    timestamp_mode = TimestampMode(args)

    assert isinstance(timestamp_mode.execute(), ValidResult)

    assert timestamp_mode.execute().result == return_stamp


def test_timestamp_mode_bad_kwargs():
    argv = 'date 34kjk3j4523k'.split()
    args = parser.parse_args(argv)

    timestamp_mode = TimestampMode(args)

    assert isinstance(timestamp_mode.execute(), InvalidResult)
