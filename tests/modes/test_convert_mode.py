import pytest

from thyme.modes import ConvertMode
from thyme.cli import parser
from thyme.results import ValidResult, InvalidResult


@pytest.mark.parametrize('argv', ['convert 20kb', 'convert 10mb'])
def test_convert_mode_init(argv):
    args = parser.parse_args(argv.split())
    cm = ConvertMode(args)
    assert cm._kwargs.command == 'convert'


@pytest.mark.parametrize('string', ['20kb', '10kb', '9000tb'])
def test_good_execute(string):
    args = parser.parse_args(['convert', string])
    cm = ConvertMode(args)
    assert isinstance(cm.execute(), ValidResult)


@pytest.mark.parametrize('argv', ['convert 1x', 'convert pz', 'convert 1'])
def test_bad_execute(argv):
    args = parser.parse_args(argv.split())
    cm = ConvertMode(args)
    assert isinstance(cm.execute(), InvalidResult)


@pytest.mark.parametrize('string', ['10KB', '10kb', '10kB'])
def test_to_string(string):
    args = parser.parse_args(['convert', string])
    cm = ConvertMode(args)
    assert cm.to_string() == 'convert 10kb'
