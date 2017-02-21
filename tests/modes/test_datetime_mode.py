import pytest

from thyme.modes import DatetimeMode
from thyme.results import ValidResult, InvalidResult

from thyme.cli import parser

in_stamp = 635904000


good_kwargs_no_format = {
    '<timestamp>': 635904000,
}

good_kwargs = {
    '<timestamp>': 635904000,
    '--format': 'YYYY MMM DD'
}

bad_kwargs = {
    '<timestamp>': '89dsljklse12'
}


def test_datetime_mode_good_kwargs_no_format():
    argv = ['date', '635904000']
    args = parser.parse_args(argv)

    timestamp_mode = DatetimeMode(args)

    res = timestamp_mode.execute()
    assert isinstance(res, ValidResult)

    assert timestamp_mode.execute().result == 'Feb 25, 1990'


def test_datetime_mode_good_kwargs_w_format():
    argv = ['date', '-fYYYY MMM DD', '635904000']
    args = parser.parse_args(argv)

    timestamp_mode = DatetimeMode(args)

    res = timestamp_mode.execute()
    assert isinstance(res, ValidResult)

    assert timestamp_mode.execute().result == '1990 Feb 25'


def test_datetime_mode_bad_kwargs():
    argv = ['date', '89dsljklse12']
    args = parser.parse_args(argv)

    timestamp_mode = DatetimeMode(args)

    res = timestamp_mode.execute()
    assert isinstance(res, InvalidResult)


def test_datetime_mode_invalid_format():
    argv = ['date', 'dsfasdfads']
    args = parser.parse_args(argv)
    timestamp_mode = DatetimeMode(args)
    res = timestamp_mode.execute()
    assert isinstance(res, InvalidResult)


def test_datetime_mode_invalid_input():
    argv = 'date 567890 --format=dsfd'.split()
    args = parser.parse_args(argv)
    dtm = DatetimeMode(args)
    with pytest.raises(ValueError):
        assert dtm._execute()
