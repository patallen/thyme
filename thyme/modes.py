from .utils import (
    datetime_to_string,
    string_to_datetime,
    make_timestamp,
    gen_random_thing,
    DenomedSize,
    format_rates,
    get_all_rates
)
from .results import ValidResult, InvalidResult


class Mode(object):
    """Mode (command) base class."""

    def __init__(self, kwargs):
        self._kwargs = kwargs

    def execute(self):
        raise NotImplementedError  # pragma: no cover


class ConvertMode(Mode):
    """Handles mode 'datetime'.

    Takes a required timestamp and optional format string.
    Returns the timestamp as a formatted date.
    """

    def execute(self):
        try:
            result = self._execute()
        except Exception as e:
            print(e)
            return InvalidResult('Unable to convert.')

        return ValidResult(result=result)

    def _execute(self):
        denomed = DenomedSize.from_string(self._kwargs.toconvert)
        in_bytes = denomed.to_bytes()
        all_rates = get_all_rates(in_bytes)
        return format_rates(all_rates)

    def _parse_input(self, value):
        for index, char in enumerate(value):
            if char not in '1234567890':
                return int(value[:index]), value[index:]
        raise ValueError("Unable to parse conversion input.")


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
        fmt = kwargs.format
        return fmt or self._default_format

    @staticmethod
    def _get_timestamp(kwargs):
        try:
            return int(kwargs.timestamp)
        except ValueError:
            raise ValueError('Timestamp must convertable to a float.')


class TimestampMode(Mode):
    """Handles mode 'timestamp'.

    Takes a required datetime and optional format string.
    Returns the datetime as a UTC timestamp.
    """

    def execute(self):
        datestring = self._kwargs.date

        return self._execute(datestring)

    @staticmethod
    def _execute(datestring):
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
        randthing = self._kwargs.type

        try:
            limit = self._kwargs.limit
        except:
            limit = 1
        return self._execute(randthing, limit)

    @staticmethod
    def _execute(randthing, limit):
        try:
            limit = int(limit)
        except TypeError:
            limit = None
        except ValueError:
            return InvalidResult("Limit must be an integer.")

        if not limit > 0:
            return InvalidResult("Limit must be greater than 0.")

        rand = gen_random_thing(randthing, limit)

        return ValidResult(result=rand)
