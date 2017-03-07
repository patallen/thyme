import os

DEFAULT_HISTORY_FILEPATH = '~/.thyme_history'
DEFAULT_HISTORY_SIZE = 50000
HISTORY_FILE_ENVAR = 'THYME_HISTORY_FILEPATH'
MAX_HISTORY_SIZE_ENVAR = 'THYME_HISTORY_SIZE'


def get_history_filepath():
    try:
        user_fp = os.environ[HISTORY_FILE_ENVAR]
        return os.path.expanduser(user_fp)
    except KeyError:
        return os.path.expanduser(DEFAULT_HISTORY_FILEPATH)


def get_max_history_size():
    try:
        size = os.environ[MAX_HISTORY_SIZE_ENVAR]
    except KeyError:
        size = DEFAULT_HISTORY_SIZE

    return int(size)
