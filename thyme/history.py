import os
import time


class ThymeException(BaseException):
    pass  # pragma: no cover


class ThymeHistory(ThymeException):
    pass  # pragma: no cover


class ThymeHistoryFileException(ThymeException):
    pass  # pragma: no cover


class HistoryFile(object):
    def __init__(self, filepath):
        try:
            with open(filepath, 'r'):
                pass
        except IOError:
            with open(filepath, 'w'):
                pass

        self.filepath = filepath
        self.encoder = HistoryCommandEncoder()

    def writeline(self, line):
        """Append any generic line to the history file."""
        with open(self.filepath, 'a') as f:
            f.write('{0}\n'.format(line))

    def write_command(self, command):
        """Write the command using the necessary Formatter."""
        encoded = self.encoder.encode(command)
        self.writeline(encoded)

    def readlines(self):
        """Get a list of lines from the history file."""
        with self._open_file('r') as f:
            lines = [l.strip('\n') for l in f.readlines()]
        return lines

    def read(self):
        """Get the command history as a single string."""
        with self._open_file('r') as f:
            whole_file = f.read()
        return whole_file

    def _open_file(self, mode='r'):
        return open(self.filepath, mode)


class HistoryCommandEncoder(object):

    def decode(self, line):
        command = line.split(':0;')[-1]
        return command

    def encode(self, command):
        command = command.to_string()
        stamp = int(time.time())
        return ': {stamp}:0;{command}'.format(stamp=stamp, command=command)


class History(object):
    def __init__(self):
        filepath = self._get_thyme_filepath()
        self.file = HistoryFile(filepath)

    def execute(self, mode, *args, **kwargs):
        """Method used to record a command.

        We take a mode <thyme.modes.Mode> and run it's `execute` method
        after writing the command to the history file.
        """
        self.file.write_command(mode)
        return mode.execute(*args, **kwargs)

    def list(self):
        """List every command in the history file."""
        history = self.file.read()
        return history

    def search(self, filter_):
        """Search history filtering on a single string."""
        history = self.file.readlines()
        filtered = [command for command in history if filter_ in command]
        return "".join(filtered)

    def _get_thyme_filepath(self):
        home = os.path.expanduser('~')
        return '{0}/.thyme_history'.format(home)
