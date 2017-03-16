from .utils import (
    datetime_to_string,
    string_to_datetime,
    make_timestamp,
    gen_random_thing,
    DenomedSize,
    format_rates,
    get_all_rates
)
from .history import History
from .results import ValidResult, InvalidResult
import os
import sys
from . import THYME_DIRECTORY


TEMPLATES = {
    "subl": 'tpl.sublime-project'
}


class Mode(object):
    """Mode (command) base class."""

    def __init__(self, kwargs):
        self._kwargs = kwargs
        self.command = kwargs.command

    def execute(self):
        raise NotImplementedError  # pragma: no cover

    def __str__(self):
        raise NotImplementedError  # pragma: no cover


class FileMode(Mode):
    def execute(self):
        try:
            result = self._execute()
        except Exception as e:
            print(e)
            return InvalidResult('Unable to create requested file.')

        return ValidResult(result=result)

    def _execute(self):
        path = sys.argv[0]
        path, filename = self._get_path_filename()
        return os.path.join(path, filename)

    def _get_path_filename(self):
        path = os.path.dirname(os.getcwd())
        name = self._kwargs.name or path.split(os.sep)[-1]
        tpl_name = get_template_from_kwargs(self._kwargs)
        extension = tpl_name.split('.')[-1]
        filename = "{}.{}".format(name, extension)
        return (path, filename)


class ConvertMode(Mode):
    """Handles mode 'datetime'.

    Takes a required timestamp and optional format string.
    Returns the timestamp as a formatted date.
    """

    def execute(self):
        try:
            result = self._execute()
        except Exception as e:
            return InvalidResult('Unable to convert.')

        return ValidResult(result=result)

    def _execute(self):
        denomed = DenomedSize.from_string(self._kwargs.toconvert)
        in_bytes = denomed.to_bytes()
        all_rates = get_all_rates(in_bytes)
        return format_rates(all_rates)

    def __str__(self):
        return '{} {}'.format(self.command, self._kwargs.toconvert).lower()


def get_template_from_kwargs(kwargs):
    print("kwargs", kwargs)
    tpl_dir = os.path.join(THYME_DIRECTORY, 'templates')
    filename = TEMPLATES[kwargs.filetype]
    return os.path.join(tpl_dir, filename)


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

    def __str__(self):
        return '{} {}'.format(self.command, self._kwargs.timestamp)


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

    def __str__(self):
        date = self._kwargs.date
        try:
            int(date)
        except ValueError:
            if ' ' in date:
                date = "'{}'".format(date)

        return '{0} {1}'.format(self.command, date)


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

    def __str__(self):
        command = self.command
        type_ = self._kwargs.type

        try:
            limit = self._kwargs.limit
        except AttributeError:
            limit = None

        if not limit:
            return '{0} {1}'.format(command, type_)

        return '{0} {1} -l{2}'.format(command, type_, limit)


class HistoryMode(Mode):
    """Handles mode 'random'.

    Returns you with a random instance of whatever was requested.
    """

    def __init__(self, *args, **kwargs):
        super(HistoryMode, self).__init__(*args, **kwargs)
        self.history = History()

    def execute(self):
        search = self._kwargs.search
        if search:
            res = self.history.search(search)

        else:
            res = self.history.list()

        return ValidResult(result=res)

    def __str__(self):
        search = self._kwargs.search
        if search:
            return "{0} '{1}'".format(self.command, search)

        return self.command
