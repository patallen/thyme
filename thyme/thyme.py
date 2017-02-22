from .modes import DatetimeMode, TimestampMode, RandomMode


class Thyme(object):
    """Main runner object. Use <instance>.run() to execute command."""

    _modes = {
        'date': DatetimeMode,
        'stamp': TimestampMode,
        'random': RandomMode
    }

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self.mode_class = self._get_mode(kwargs)

    def _get_mode(self, kwargs):
        return self._modes[kwargs.command]

    def run(self):
        self.mode = self.mode_class(self._kwargs)
        res = self.mode.execute()
        print(res)
