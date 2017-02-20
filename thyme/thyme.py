from modes import DatetimeMode, TimestampMode


class Thyme(object):
    _modes = {
        'date': DatetimeMode,
        'stamp': TimestampMode,
        # 'random': RandomMode
    }

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self.mode_class = self._get_mode(kwargs)

    def _get_mode(self, kwargs):
        for mode in self._modes.keys():
            if kwargs.get(mode, False):
                return self._modes[mode]

        # check if --version or --help here
        print "Did not supply a valid mode. Use 'thyme -h' for help."

    def run(self):
        self.mode = self.mode_class(self._kwargs)
        res = self.mode.execute()
        print res
