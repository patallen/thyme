from thyme.modes import RandomMode
from thyme.results import ValidResult, InvalidResult


from thyme.cli import parser


def test_random_mode_init():
    argv = 'random uuid'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    assert rm._kwargs.type == 'uuid'


def test_random_mode_uuid():
    argv = 'random uuid'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert len(str(res.result)) == 36
    assert '-' in str(res)


def test_random_mode_int():
    argv = 'random int -l10000'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, int)
    assert res.result <= 10000
    assert '.' not in str(res.result)


def test_random_mode_float():
    argv = 'random float -l10000'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, float)
    assert res.result <= 10000
    assert '.' in str(res.result)


def test_random_mode_secret():
    argv = ['random', 'secret', '-l 100']
    args = parser.parse_args(argv)
    rm = RandomMode(args)
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, str)
    assert len(res.result) == 100


def test_random_mode_invalid_limit():
    argv = 'random float -l-100000'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    res = rm.execute()
    assert isinstance(res, InvalidResult)
    assert res.errors[0] == 'Limit must be greater than 0.'

    argv = 'random float -l90.09'
    args = parser.parse_args(argv.split())
    rm = RandomMode(args)
    res = rm.execute()
    assert isinstance(res, InvalidResult)
    assert res.errors[0] == 'Limit must be an integer.'
