from datetime import date as d

from utils import convert_fmt

from lol import lolololololololololololololololololol


class InvalidResult(object):
    def __init__(self, errors=None):
        self.errors = []

    def add_error(self, category, error):
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0

    @classmethod
    def from_list(cls, errors):
        result = cls(
            errors=errors
        )
        return result

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__


class ValidResult(object):
    def __init__(self, result, message=None):
        self.result = result
        self.message = message or lolololololololololololololololololol()

    def __bool__(self):
        return True

    def __str__(self):
        return "%s\n%s" % (self.message, self.result)

    __nonzero__ = __bool__


class Command(object):
    """Base Command class. Do not instantiate."""
    COMMAND_STRING = None

    def __init__(self, args):
        self.args = args
        self.invalid_result = InvalidResult()

    def execute(self):
        raise NotImplementedError


class FromDatetimeCommand(Command):
    def execute(self):
        pass


class FromTimestampCommand(Command):

    def execute(self):
        result = self._get_result()
        return result

    def _get_result(self):
        try:
            date = d.fromtimestamp(self.args.datething)
        except ValueError as e:
            return InvalidResult.from_list([{
                'category': 'timestamp',
                'message': e.error
            }])

        try:
            fmt = self._get_format()
        except ValueError as e:
            return InvalidResult.from_list([{
                'category': 'format',
                'message': e.message
            }])

        return ValidResult(date.strftime(fmt))

    def _get_format(self):
        try:
            return convert_fmt(self.args.format)
        except:
            raise ValueError("Could not decipher the specified format.")
