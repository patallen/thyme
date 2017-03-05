from thyme.modes import HistoryMode
from thyme.history import History
from thyme.results import ValidResult, InvalidResult
try:
    from unittest import mock
except ImportError:
    import mock

from thyme.cli import parser


def test_random_mode_init():
    argv = 'history'
    args = parser.parse_args(argv.split())
    hm = HistoryMode(args)

    assert hm._kwargs.search is None
    assert hm._kwargs.command == 'history'
    assert isinstance(hm.history, History)


def test_to_string():
    argv = ['history']
    args = parser.parse_args(argv)
    hm = HistoryMode(args)
    assert hm.to_string() == 'history'

    argv = ['history', 'blue man group']
    args = parser.parse_args(argv)
    hm = HistoryMode(args)

    assert hm.to_string() == "history 'blue man group'"


@mock.patch('thyme.history.History.list', return_value='boo\nbah\n')
@mock.patch('thyme.history.HistoryFile.readlines', return_value=['boo', 'bah'])
def test_history_mode_execute(mock_list, mock_search):
    argv = ['history']
    args = parser.parse_args(argv)
    hm = HistoryMode(args)
    assert hm.execute().result == 'boo\nbah\n'

    argv = ['history', 'boo']
    args = parser.parse_args(argv)
    hm = HistoryMode(args)
    assert hm.execute().result == 'boo'