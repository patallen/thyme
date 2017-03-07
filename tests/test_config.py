import os
import pytest
from thyme import config


@pytest.fixture
def reset_env(request):
    def reset():
        os.environ = {}
    reset()
    request.addfinalizer(reset)


def test_get_max_history_size(reset_env):
    size = config.get_max_history_size()
    assert size == 50000

    os.environ[config.MAX_HISTORY_SIZE_ENVAR] = '10'
    size = config.get_max_history_size()
    assert size == 10


def test_get_history_filepath(reset_env):
    fp = config.get_history_filepath()
    assert fp == os.path.expanduser('~/.thyme_history')

    os.environ[config.HISTORY_FILE_ENVAR] = '~/roodeejoolyawni'
    fp = config.get_history_filepath()
    assert fp == os.path.expanduser('~/roodeejoolyawni')

    os.environ[config.HISTORY_FILE_ENVAR] = 'boobobeboo'
    fp = config.get_history_filepath()
    assert fp == 'boobobeboo'
