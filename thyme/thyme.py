import os


from .modes import DatetimeMode, TimestampMode, RandomMode, ConvertMode, HistoryMode
from .history import History


class Thyme(object):
    """Main runner object. Use <instance>.run() to execute command."""

    _modes = {
        'date': DatetimeMode,
        'stamp': TimestampMode,
        'random': RandomMode,
        'convert': ConvertMode,
        'history': HistoryMode
    }

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self.mode_class = self._get_mode(kwargs)
        self.history = History()

    def _get_mode(self, kwargs):
        return self._modes[kwargs.command]

    def run(self):
        self.mode = self.mode_class(self._kwargs)
        res = self.history.execute(self.mode)
        print(res)
