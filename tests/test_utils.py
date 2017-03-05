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


def test_denomed_size():
    kb_denom = utils.DenomedSize.from_string('10kb')
    mb_denom = utils.DenomedSize.from_string('10mb')
    gb_denom = utils.DenomedSize.from_string('10gb')
    tb_denom = utils.DenomedSize.from_string('10tb')
    pb_denom = utils.DenomedSize.from_string('10pb')

    assert kb_denom.to_bytes() == 10240
    assert mb_denom.to_bytes() == 10485760
    assert gb_denom.to_bytes() == 10737418240
    assert tb_denom.to_bytes() == 10995116277760
    assert pb_denom.to_bytes() == 11258999068426240


def test_denomed_size_non_lowercase():
    kb_denom = utils.DenomedSize.from_string('10KB')
    assert kb_denom.to_bytes() == 10240


def test_invalid_denomed_size_string():
    with pytest.raises(ValueError):
        utils.DenomedSize.from_string('10badbad')


def test_get_all_rates():
    bytes_ = 9000.0
    rates = utils.get_all_rates(bytes_)

    expected = [
        (bytes_, 'b'), (bytes_ / 1024, 'kb'), (bytes_ / 1048576, 'mb'),
        (bytes_ / 1073741824, 'gb'), (bytes_ / 1099511627776, 'tb'),
        (bytes_ / 1125899906842624, 'pb')
    ]

    assert rates == expected


def test__parse_size_string():
    expected = (10, 'kb')
    assert expected == utils._parse_size_string('10kb')

    with pytest.raises(ValueError):
        utils._parse_size_string('12345')


def test_format_rates():
    rates = utils.get_all_rates(9000.0)
    expected = ("    Bytes:  9000\n"
                "Kilobytes:  8.78906\n"
                "Megabytes:  0.00858307\n"
                "Gigabytes:  8.3819e-06\n"
                "Terabytes:  8.18545e-09\n"
                "Petabytes:  7.99361e-12")

    assert utils.format_rates(rates) == expected
