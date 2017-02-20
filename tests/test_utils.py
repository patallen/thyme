import pytest
from datetime import datetime

from thyme.utils import string_to_datetime, make_timestamp, datetime_to_string

good_dates = [
    'February 25 1990',
    '02/25/1990',
    '02-25-1990',
    'Feb 25 1990',
    'Feb 25, 1990',
    '2/25/90',
    '2-25-90',
    '02251990',
]

bad_dates = [
    'zz3234z',
    'feb 25 190'
]


def test_string_to_datetime():
    final = datetime(1990, 2, 25)

    for good_date in good_dates:
        assert string_to_datetime(good_date) == final


def test_bad_date_string():
    for bad_date in bad_dates:
        with pytest.raises(ValueError):
            string_to_datetime(bad_date)


def test_good_make_timestamp():
    date = datetime(1990, 2, 25)
    ts = 635904000

    assert make_timestamp(date) == ts


def test_bad_make_timestamp():
    date = 'not a datetime'

    with pytest.raises(TypeError):
        make_timestamp(date)


def test_datetime_to_string():
    dt = datetime(1990, 2, 25)
    string = datetime_to_string(dt, 'MMM DD, YYYY')
    assert string == 'Feb 25, 1990'

    string = datetime_to_string(dt, 'mmm dd, yyyy')
    assert string == 'Feb 25, 1990'
