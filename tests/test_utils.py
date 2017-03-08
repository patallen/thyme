import pytest
from datetime import datetime

from thyme import utils


GOOD_STRINGS = [
    'February 25 1990', '02/25/1990', '02-25-1990',
    'Feb 25 1990', 'Feb 25, 1990', '2/25/90', '2-25-90',
]


@pytest.mark.parametrize('string', GOOD_STRINGS)
def test_string_to_datetime(string):
    assert utils.string_to_datetime(string) == datetime(1990, 2, 25)


@pytest.mark.parametrize('dt', ['zz3234z', '02251990'])
def test_bad_date_string(dt):
    with pytest.raises(ValueError):
        utils.string_to_datetime(dt)


def test_good_make_timestamp():
    date = datetime(1990, 2, 25)
    assert utils.make_timestamp(date) == 635904000


@pytest.mark.parametrize('dt', (100, 'xyz', 9.9, 'Feb, 25'))
def test_invalid_datetime_make_timestamp(dt):
    with pytest.raises(TypeError):
        utils.make_timestamp(dt)


@pytest.mark.parametrize('fmt', ('MMM DD, YYYY', 'mmm dd, yyyy'))
def test_datetime_to_string(fmt):
    dt = datetime(1990, 2, 25)
    assert utils.datetime_to_string(dt, fmt) == 'Feb 25, 1990'


@pytest.mark.parametrize('alist, ex', [
    ((1, 2, 3), False), ((1, 1, 1), True), ((1,), True)
])
def test_assert_all_equal(alist, ex):
    assert utils.assert_all_equal(alist) == ex


@pytest.mark.parametrize('fmt, expected', [
    ('YYY MMM DD', True), ('YZYY MMM D', False)
])
def test_validate_format(fmt, expected):
    assert utils._validate_format(fmt) == expected


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


@pytest.mark.parametrize('string, expected', [
    ('10kb', 10240), ('10mb', 10485760), ('10gb', 10737418240),
    ('10tb', 10995116277760), ('10pb', 11258999068426240)
])
def test_denomed_size(string, expected):
    res = utils.DenomedSize.from_string(string).to_bytes()
    assert res == expected


@pytest.mark.parametrize('string', ['10kB', '10KB', '10Kb'])
def test_denomed_size_non_lowercase(string):
    assert utils.DenomedSize.from_string(string).to_bytes() == 10240


@pytest.mark.parametrize('string', ('10bad', '10x', 'zz', 'z10'))
def test_invalid_denomed_size_string(string):
    with pytest.raises(ValueError):
        utils.DenomedSize.from_string(string)


def test_get_all_rates():
    bytes_ = 9000.0
    rates = utils.get_all_rates(bytes_)

    expected = [
        (bytes_, 'b'), (bytes_ / 1024, 'kb'), (bytes_ / 1048576, 'mb'),
        (bytes_ / 1073741824, 'gb'), (bytes_ / 1099511627776, 'tb'),
        (bytes_ / 1125899906842624, 'pb')
    ]

    assert rates == expected


@pytest.mark.parametrize('string, expected', (
    ('10kb', (10, 'kb')), ('10mb', (10, 'mb')),
))
def test__parse_size_string(string, expected):
    assert expected == utils._parse_size_string(string)


@pytest.mark.parametrize('string', ('zbc', 'xx10', 100))
def test__parse_size_string_invalid(string):
    with pytest.raises(ValueError):
        utils._parse_size_string(string)


def test_format_rates():
    rates = utils.get_all_rates(9000.0)
    expected = ("    Bytes:  9000\n"
                "Kilobytes:  8.78906\n"
                "Megabytes:  0.00858307\n"
                "Gigabytes:  8.3819e-06\n"
                "Terabytes:  8.18545e-09\n"
                "Petabytes:  7.99361e-12")

    assert utils.format_rates(rates) == expected
