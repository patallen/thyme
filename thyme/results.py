from .lol import lolololololololololololololololololol


class InvalidResult(object):
    def __init__(self, error=None, errors=None):
        self.errors = errors or []
        if error:
            self.errors = [error]

    def add_error(self, error):
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

    def __str__(self):
        woops = 'Whoops! We couldn\'t do that...\n'

        msg = "%s%s" % (woops, "\n".join([n for n in self.errors]))
        return msg

    __bool__ = __nonzero__


class ValidResult(object):
    def __init__(self, result, message=None):
        self.result = result
        self.message = message  or lolololololololololololololololololol()

    def __bool__(self):
        return True

    def __str__(self):
        return "\n%s -- %s\n" % (self.result, self.message)

    __nonzero__ = __bool__