import pytest

from thyme.modes import DatetimeMode
from thyme.results import ValidResult, InvalidResult


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
    kwargs = {
        '<timestamp>': 635904000,
    }
    timestamp_mode = DatetimeMode(kwargs)

    res = timestamp_mode.execute()
    assert isinstance(res, ValidResult)

    assert timestamp_mode.execute().result == 'Feb 25, 1990'


def test_datetime_mode_good_kwargs_w_format():
    kwargs = {
        '<timestamp>': 635904000,
        '--format': 'YYYY MMM DD'
    }
    timestamp_mode = DatetimeMode(kwargs)

    res = timestamp_mode.execute()
    assert isinstance(res, ValidResult)

    assert timestamp_mode.execute().result == '1990 Feb 25'


def test_datetime_mode_bad_kwargs():
    kwargs = {
        '<timestamp>': '89dsljklse12'
    }
    timestamp_mode = DatetimeMode(kwargs)

    res = timestamp_mode.execute()
    assert isinstance(res, InvalidResult)


def test_datetime_mode_invalid_format():

    kwargs = {
        '<timestamp>': 635904000,
        '--format': 'zlkfjldsakfj'
    }
    timestamp_mode = DatetimeMode(kwargs)
    res = timestamp_mode.execute()
    assert isinstance(res, InvalidResult)


def test_datetime_mode_invalid_input():
    dtm = DatetimeMode({'<timestamp>': 'z'})
    with pytest.raises(ValueError):
        assert dtm._execute()
