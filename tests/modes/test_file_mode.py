import os
from thyme.modes import get_template_from_kwargs
from thyme import THYME_DIRECTORY
import mock


def test_get_template_from_kwargs():
    kwargs = mock.MagicMock()
    kwargs.filetype = "sublime"
    tpl = get_template_from_kwargs(kwargs)
    assert tpl == os.path.join(THYME_DIRECTORY,
                               'templates',
                               'tpl.sublime-project')
