from datetime import date as d
from utils import get_strftime_format, string_to_datetime, make_timestamp
from results import ValidResult, InvalidResult


class Mode(object):

    def __init__(self, kwargs):
        self._kwargs = kwargs

    def execute(self):
        raise NotImplementedError


class DatetimeMode(Mode):
    """Handles mode 'datetime'.


    Takes a required timestamp and optional format string.
    Returns the timestamp as a formatted date.
    """
    _default_format = 'mm/dd/yyyy'

    def execute(self):
        timestamp = self._get_timestamp(self._kwargs)
        dateformat = self._get_format(self._kwargs)

        return self._execute(timestamp, dateformat)

    def _execute(self, timestamp, dateformat):
        try:
            date = d.fromtimestamp(timestamp)
        except Exception as e:
            return InvalidResult(error={'category': 'invalid', 'error': e})

        fmt = get_strftime_format(dateformat)

        try:
            formatted = date.strftime(fmt)
        except Exception as e:
            return InvalidResult({'category': 'formatting', 'error': e})

        return ValidResult(result=formatted)

    def _get_format(self, kwargs):
        f1 = kwargs.get('--format')
        f2 = kwargs.get('-f')
        return f1 or f2 or self._default_format

    def _get_timestamp(self, kwargs):
        ts = float(kwargs.get('<timestamp>'))
        if not ts:
            raise TypeError('Timestamp cannot be None.')

        return float(ts)


class TimestampMode(Mode):
    """Handles mode 'datetime'.


    Takes a required datetime and optional format string.
    Returns the datetime as a UTC timestamp.
    """

    def execute(self):
        datestring = self._kwargs['<datestring>']

        return self._execute(datestring)

    def _execute(self, datestring):
        try:
            dt = string_to_datetime(datestring)
        except:
            return InvalidResult(
                {'category': 'invalid',
                 'error': 'Could not handle date string.'}
            )

        try:
            timestamp = make_timestamp(dt)
        except:
            return InvalidResult(
                {'category': 'other',
                 'error': 'Could not make timestamp from datetime.'}
            )

        return ValidResult(result=timestamp)
