from thyme.modes import TimestampMode
from thyme.results import ValidResult, InvalidResult


date_string = 'feb 25 1990'
return_stamp = 635904000

good_kwargs = {
    '<datestring>': 'feb 25 1990',
}

bad_kwargs = {
    '<datestring>': '89dsljklse12'
}


def test_timestamp_mode_good_kwargs():
    timestamp_mode = TimestampMode(good_kwargs)

    assert isinstance(timestamp_mode.execute(), ValidResult)

    assert timestamp_mode.execute().result == return_stamp


def test_timestamp_mode_bad_kwargs():
    timestamp_mode = TimestampMode(bad_kwargs)

    assert isinstance(timestamp_mode.execute(), InvalidResult)