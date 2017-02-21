import pytest
from datetime import datetime

from thyme.utils import (
    string_to_datetime,
    make_timestamp,
    datetime_to_string,
    assert_all_equal,
    gen_random_thing,
    _validate_format,
    _random_secret
)

good_dates = [
    'February 25 1990',
    '02/25/1990',
    '02-25-1990',
    'Feb 25 1990',
    'Feb 25, 1990',
    '2/25/90',
    '2-25-90',
]

bad_dates = [
    'zz3234z',
    '02251990',
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


def test_assert_all_equal():
    good = ['a', 'a', 'a']
    assert assert_all_equal(good)

    bad = ['a', 'b', 'c']
    assert not assert_all_equal(bad)

    one = ['a']
    assert assert_all_equal(one)


def test_validate_format():
    good = 'YYYY MMM DD'
    bad = 'YZYY MMM D'

    assert _validate_format(good)
    assert not _validate_format(bad)


def test_gen_random_thing_uuid():
    thing = gen_random_thing('uuid')
    assert len(str(thing)) == 36
    assert '-' in str(thing)


def test_gen_random_thing_float():
    thing = gen_random_thing('float')
    assert type(thing) == float
    assert '.' in str(thing)


def test_gen_random_thing_int():
    thing = gen_random_thing('int')
    assert type(thing) == int
    assert '.' not in str(thing)


def test__random_secret():
    sec = _random_secret()
    assert len(sec) == 64
    assert isinstance(sec, str)

    sec = _random_secret(24)
    assert len(sec) == 24
    assert isinstance(sec, str)
