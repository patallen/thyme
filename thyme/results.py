
class InvalidResult(object):
    """This result should be returned when the action was not successful.

    It is also the vehicle for storing and displaying any errors that it
    has accrued.
    """

    def __init__(self, error=None, errors=None):
        self.errors = errors or []
        if error:
            self.errors = [error]

    def add_error(self, error):
        """Add an error string to the list of errors."""
        self.errors.append(error)

    def has_errors(self):
        """Identifiy whether the instance has errors set."""
        return len(self.errors) > 0

    @classmethod
    def from_list(cls, errors):
        """Create a new instance from a list of errors."""
        result = cls(errors=errors)
        return result

    def __bool__(self):
        """bool(result) should always return False."""
        return False

    def __str__(self):
        """Display the error when printed.

        TODO: Find a way to display the correct help screen instead.
        """
        woops = 'Whoops! We couldn\'t do that...\n'

        msg = "{0}{1}".format(woops, "\n".join(n for n in self.errors))
        return msg

    __nonzero__ = __bool__


class ValidResult(object):
    """This result should be returned when the action was successful."""

    def __init__(self, result, message=None):
        self.result = result
        self.message = message

    def __bool__(self):
        """bool(result) should always return True."""
        return True

    def __str__(self):
        """Display the result when printed."""
        return '\n{0}\n'.format(self.result)

    __nonzero__ = __bool__
