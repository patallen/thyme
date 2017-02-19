import pytest

from thyme.utils import convert_fmt, _find_delimiter, _find_parts

good_no_delim_formats = ['yyyymmdd', 'mmddyyyy']
acceptable_no_delim_formats = ['yyymmmdd', 'mmmddyyy']
should_raise_no_delim_formats = ['ymd', 'yearmonthday']


def test_find_good_no_delim_parts():
    parts = _find_parts(good_no_delim_formats[0])

    assert parts == ['yyyy', 'mm', 'dd']

    parts = _find_parts(good_no_delim_formats[1])

    assert parts == ['mm', 'dd', 'yyyy']


def test_find_acceptable_no_delim_parts():
    parts = _find_parts(acceptable_no_delim_formats[0])

    assert parts == ['yy', 'mm', 'dd']

    parts = _find_parts(acceptable_no_delim_formats[1])

    assert parts == ['mm', 'dd', 'yy']


def test_should_raise_error():
    with pytest.raises(ValueError):
        _find_parts(should_raise_no_delim_formats[0])

    with pytest.raises(ValueError):
        _find_parts(should_raise_no_delim_formats[1])


def test_convert_fmt():
    fmt = 'yyyy-mm-dd'
    assert convert_fmt(fmt) == '%Y-%m-%d'

    fmt = 'mm-yy-dd'
    assert convert_fmt(fmt) == '%m-%y-%d'

    fmt = 'dd/mm/yyyy'
    assert convert_fmt(fmt) == '%d/%m/%Y'


def test_convert_fmt_no_delim():
    fmt = 'yyyymmdd'
    assert convert_fmt(fmt) == '%Y%m%d'
