import os
from thyme import config


def test_get_max_history_size():
    size = config.get_max_history_size()
    assert size == 50000

    os.environ[config.MAX_HISTORY_SIZE_ENVAR] = '10'
    size = config.get_max_history_size()
    assert size == 10


def test_get_history_filepath():
    fp = config.get_history_filepath()
    assert fp == os.path.expanduser('~/.thyme_history')

    os.environ[config.HISTORY_FILE_ENVAR] = '~/roodeejoolyawni'
    fp = config.get_history_filepath()
    assert fp == os.path.expanduser('~/roodeejoolyawni')

    os.environ[config.HISTORY_FILE_ENVAR] = 'boobobeboo'
    fp = config.get_history_filepath()
    assert fp == 'boobobeboo'
