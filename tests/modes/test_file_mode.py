import os
import pytest
import mock

from thyme import THYME_DIRECTORY
from thyme.cli import parser
from thyme.modes import get_template_from_kwargs, FileMode


def test_get_template_from_kwargs():
    kwargs = mock.MagicMock()
    kwargs.filetype = "subl"
    tpl = get_template_from_kwargs(kwargs)
    assert tpl == os.path.join(THYME_DIRECTORY,
                               'templates',
                               'tpl.sublime-project')


@pytest.mark.parametrize('args',
                         ('file subl -nthyme',
                          'file subl',
                          'file subl --name=hello'))
def test_file_mode_cli(args):
    args = args.split(' ')
    try:
        parser.parse_args(args)
    except SystemExit:
        pytest.fail("Should not raise a SystemExit exception.")


@pytest.mark.parametrize(
    'args, expected',
    (('file subl -nthyme', ('file', 'subl', 'thyme')),
     ('file subl', ('file', 'subl', None)))
)
def test_file_mode_init(args, expected):
    args = args.split(' ')
    args = parser.parse_args(args)
    fm = FileMode(args)

    assert fm.command == expected[0]
    assert fm._kwargs.filetype == expected[1]
    assert fm._kwargs.name == expected[2]


@pytest.mark.parametrize(
    'args, fname',
    (('file subl -nthyme', 'thyme.sublime-project'),
     ('file subl', 'c.sublime-project'))
)
@mock.patch('os.getcwd', return_value='/a/b/c')
@mock.patch('shutil.copy', return_value=None)
def test_execute_returns_path(m, mock_cwd, args, fname):
    args = args.split(' ')
    args = parser.parse_args(args)
    fm = FileMode(args)
    res = fm.execute()
    assert os.path.join('/a/b/c', fname) in res.result
