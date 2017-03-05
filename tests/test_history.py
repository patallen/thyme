import os

try:
    from unittest import mock
except ImportError:
    import mock

from thyme.history import History, HistoryFile, HistoryCommandEncoder

TEMP_PATH = '/tmp/temp'


def remove_temp():
    os.remove(TEMP_PATH)


def test_history_file():
    file = HistoryFile(TEMP_PATH)
    assert file.filepath == TEMP_PATH

    assert 'temp' in os.listdir('/tmp')

    assert file.encoder is not None
    remove_temp()


def test_readlines():
    file = HistoryFile(TEMP_PATH)
    with open('/tmp/temp', 'w') as f:
        f.write('boo who\n')
        f.write('bo ho\n')

    assert file.readlines() == ['boo who', 'bo ho']
    remove_temp()


def test_read():
    file = HistoryFile(TEMP_PATH)
    with open('/tmp/temp', 'w') as f:
        f.write('boo who\n')
        f.write('bo ho\n')

    assert file.read() == 'boo who\nbo ho\n'
    remove_temp()


def test_write_command():
    file = HistoryFile(TEMP_PATH)
    file.writeline = mock.MagicMock()
    command = mock.MagicMock()
    command.to_string = mock.MagicMock(return_value='dude')

    file.write_command(command)
    assert file.writeline.called
    remove_temp()


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


@mock.patch('thyme.history.History._get_thyme_filepath', return_value=TEMP_PATH)
def test_history_list(mock_path):
    with open(TEMP_PATH, 'w') as f:
        f.write('hello\nworkd\n')

    history = History()
    assert history.list() == 'hello\nworkd\n'
    remove_temp()


@mock.patch('thyme.history.History._get_thyme_filepath', return_value=TEMP_PATH)
def test_history_search(mock_path):
    with open(TEMP_PATH, 'w') as f:
        f.write('hello\nworkd\n')

    history = History()
    assert history.search('llo') == 'hello'
