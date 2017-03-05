import pytest
from datetime import datetime

from thyme import utils

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
        assert utils.string_to_datetime(good_date) == final


def test_bad_date_string():
    for bad_date in bad_dates:
        with pytest.raises(ValueError):
            utils.string_to_datetime(bad_date)


def test_good_make_timestamp():
    date = datetime(1990, 2, 25)
    ts = 635904000

    assert utils.make_timestamp(date) == ts


def test_bad_make_timestamp():
    date = 'not a datetime'

    with pytest.raises(TypeError):
        utils.make_timestamp(date)


def test_datetime_to_string():
    dt = datetime(1990, 2, 25)
    string = utils.datetime_to_string(dt, 'MMM DD, YYYY')
    assert string == 'Feb 25, 1990'

    string = utils.datetime_to_string(dt, 'mmm dd, yyyy')
    assert string == 'Feb 25, 1990'


def test_assert_all_equal():
    good = ['a', 'a', 'a']
    assert utils.assert_all_equal(good)

    bad = ['a', 'b', 'c']
    assert not utils.assert_all_equal(bad)

    one = ['a']
    assert utils.assert_all_equal(one)


def test_validate_format():
    good = 'YYYY MMM DD'
    bad = 'YZYY MMM D'

    assert utils._validate_format(good)
    assert not utils._validate_format(bad)


def test_gen_random_thing_uuid():
    thing = utils.gen_random_thing('uuid')
    assert len(str(thing)) == 36
    assert '-' in str(thing)


def test_gen_random_thing_float():
    thing = utils.gen_random_thing('float')
    assert type(thing) == float
    assert '.' in str(thing)


def test_gen_random_thing_int():
    thing = utils.gen_random_thing('int')
    assert type(thing) == int
    assert '.' not in str(thing)


def test_random_secret():
    sec = utils.random_secret()
    assert len(sec) == 64
    assert isinstance(sec, str)

    sec = utils.random_secret(24)
    assert len(sec) == 24
    assert isinstance(sec, str)


def test_to_bytes():
    bs = utils.to_bytes(10, 'b')
    assert bs == 10

    expected = bs * 1024
    bs = utils.to_bytes(10, 'kb')
    assert bs == expected

    expected = bs * 1024
    bs = utils.to_bytes(10, 'mb')
    assert bs == expected

    expected = bs * 1024
    bs = utils.to_bytes(10, 'gb')
    assert bs == expected

    expected = bs * 1024
    bs = utils.to_bytes(10, 'tb')
    assert bs == expected

    expected = bs * 1024
    bs = utils.to_bytes(10, 'pb')
    assert bs == expected


def test_to_bytes_invalid():
    with pytest.raises(ValueError):
        utils.to_bytes(10, 'notvalid')


def test_get_all_rates():
    bytes_ = 10
    rates = utils.get_all_rates(bytes_)

    expected = [
        (10, 'b'), (10240, 'kb'), (10485760, 'mb'), (10737418240, 'gb'),
        (10995116277760, 'tb'), (11258999068426240, 'pb')
    ]

    assert rates == expected


def test_format_rates():
    rates = utils.get_all_rates(10)
    expected = ("Bytes:\t10\nKilobytes:\t10240\nMegabytes:\t10485760\n"
                "Gigabytes:\t10737418240\nTerabytes:\t10995116277760\n"
                "Petabytes:\t11258999068426240")

    assert utils.format_rates(rates) == expected
