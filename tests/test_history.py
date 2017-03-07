import os
import pytest


try:
    from unittest import mock
except ImportError:
    import mock

from thyme.history import History, HistoryFile, HistoryCommandEncoder

TEMP_PATH = '/tmp/temp'


@pytest.fixture()
def remove_temp(request):
    request.addfinalizer(lambda: os.remove(TEMP_PATH))


def test_history_file(remove_temp):
    file = HistoryFile(TEMP_PATH, 200)
    assert file.filepath == TEMP_PATH

    assert 'temp' in os.listdir('/tmp')

    assert file.encoder is not None


def test_readlines(remove_temp):
    file = HistoryFile(TEMP_PATH, 200)
    with open('/tmp/temp', 'w') as f:
        f.write('boo who\n')
        f.write('bo ho\n')

    assert file.readlines() == ['boo who', 'bo ho']


def test_read(remove_temp):
    file = HistoryFile(TEMP_PATH, 200)
    with open('/tmp/temp', 'w') as f:
        f.write('boo who\n')
        f.write('bo ho\n')

    assert file.read() == 'boo who\nbo ho\n'


def test_write_command(remove_temp):
    file = HistoryFile(TEMP_PATH, 200)
    file.writeline = mock.MagicMock()
    command = mock.MagicMock()
    command.to_string = mock.MagicMock(return_value='dude')

    file.write_command(command)
    assert file.writeline.called


@mock.patch('time.time', return_value=100)
def test_historycommandencoder_encode(mock_time):
    hce = HistoryCommandEncoder()
    command = mock.MagicMock()
    command.to_string = mock.MagicMock(return_value='go charlie')
    encoded = hce.encode(command)
    assert encoded == ': 100:0;go charlie'


def test_historycommandencoder_decode():
    hce = HistoryCommandEncoder()
    encoded = ': 100:0;go charlie'
    decoded = hce.decode(encoded)
    assert decoded == 'go charlie'


@mock.patch('thyme.config.get_history_filepath', return_value=TEMP_PATH)
def test_history_list(mock_path, remove_temp):
    with open(TEMP_PATH, 'w') as f:
        f.write('hello\nworkd\n')

    history = History()
    assert history.list() == 'hello\nworkd\n'


@mock.patch('thyme.config.get_history_filepath', return_value=TEMP_PATH)
def test_history_search(mock_path, remove_temp):
    with open(TEMP_PATH, 'w') as f:
        f.write('hello\nworkd\n')

    history = History()
    assert history.search('llo') == 'hello'


def test_truncate_history_file(remove_temp):
    hf = HistoryFile(TEMP_PATH, 3)

    obj = mock.MagicMock()
    obj.to_string = mock.MagicMock(return_value='my little pony')

    for l in range(5):
        hf.write_command(obj)

    with open(TEMP_PATH) as f:
        file_len = len(f.readlines())

    assert file_len == 3
