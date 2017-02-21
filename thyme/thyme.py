from .modes import DatetimeMode, TimestampMode, RandomMode


class Thyme(object):
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

        # check if --version or --help here
        print("Did not supply a valid mode. Use 'thyme -h' for help.")

    def run(self):
        self.mode = self.mode_class(self._kwargs)
        res = self.mode.execute()
        print(res)
