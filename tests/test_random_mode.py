from thyme.modes import RandomMode
from thyme.results import ValidResult, InvalidResult


def test_random_mode_init():
    rm = RandomMode({'<randthing>': 'uuid', '<limit>': None})
    assert rm._kwargs['<randthing>'] == 'uuid'
    assert rm._kwargs['<limit>'] is None


def test_random_mode_uuid():
    rm = RandomMode({'<randthing>': 'uuid', '<limit>': 10000})
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert len(str(res.result)) == 36
    assert '-' in str(res)


def test_random_mode_int():
    rm = RandomMode({'<randthing>': 'int', '<limit>': 10000})
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, int)
    assert res.result <= 10000
    assert '.' not in str(res.result)


def test_random_mode_float():
    rm = RandomMode({'<randthing>': 'float', '<limit>': 10000})
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, float)
    assert res.result <= 10000
    assert '.' in str(res.result)


def test_random_mode_secret():
    rm = RandomMode({'<randthing>': 'secret', '<limit>': 100})
    res = rm.execute()

    assert isinstance(res, ValidResult)
    assert isinstance(res.result, str)
    assert len(res.result) == 100


def test_random_mode_invalid_thing():
    rm = RandomMode({'<randthing>': 'sdfdsdfg'})
    res = rm.execute()

    assert isinstance(res, InvalidResult)
