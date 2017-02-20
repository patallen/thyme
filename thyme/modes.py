from .utils import (
    datetime_to_string,
    string_to_datetime,
    make_timestamp,
    gen_random_thing,
)
from .results import ValidResult, InvalidResult


class Mode(object):

    def __init__(self, kwargs):
        self._kwargs = kwargs

    def execute(self):
        raise NotImplementedError  # pragma: no cover


class DatetimeMode(Mode):
    """Handles mode 'datetime'.

    Takes a required timestamp and optional format string.
    Returns the timestamp as a formatted date.
    """

    _default_format = 'MMM DD, YYYY'

    def execute(self):
        try:
            result = self._execute()
        except Exception:
            return InvalidResult('Could not process timestamp.')

        return ValidResult(result=result)

    def _execute(self):
        from datetime import datetime as dt
        timestamp = self._get_timestamp(self._kwargs)
        dateformat = self._get_format(self._kwargs)
        date = dt.utcfromtimestamp(timestamp)
        formatted = datetime_to_string(date, dateformat)
        return formatted

    def _get_format(self, kwargs):
        f1 = kwargs.get('--format')
        f2 = kwargs.get('-f')
        return f1 or f2 or self._default_format

    def _get_timestamp(self, kwargs):
        try:
            return float(kwargs.get('<timestamp>'))
        except ValueError:
            raise ValueError('Timestamp must convertable to a float.')


class TimestampMode(Mode):
    """Handles mode 'timestamp'.

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
            return InvalidResult('Could not handle date string')

        timestamp = make_timestamp(dt)

        return ValidResult(result=timestamp)


class RandomMode(Mode):
    """Handles mode 'random'.

    Returns you with a random instance of whatever was requested.
    """

    def execute(self):
        randthing = self._kwargs['<randthing>']
        limit = self._kwargs.get('<limit>') or 100

        return self._execute(randthing, limit)

    def _execute(self, randthing, limit):
        try:
            limit = int(limit)
        except ValueError:
            return InvalidResult("Limit must be an integer.")

        if not limit > 0:
            return InvalidResult("Limit must be greater than 0.")

        try:
            rand = gen_random_thing(randthing, limit)
        except ValueError:
            return InvalidResult("couldn't do it.")

        return ValidResult(result=rand)
