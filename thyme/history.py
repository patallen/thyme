import time
from . import config


class ThymeException(BaseException):
    pass  # pragma: no cover


class ThymeHistory(ThymeException):
    pass  # pragma: no cover


class ThymeHistoryFileException(ThymeException):
    pass  # pragma: no cover


class HistoryFile(object):
    def __init__(self, filepath, max_length):
        self._ensure_file(filepath)
        self.max_length = max_length
        self.filepath = filepath
        self.encoder = HistoryCommandEncoder()

    def writeline(self, line):
        """Append any generic line to the history file."""
        with open(self.filepath, 'a') as f:
            f.write('{0}\n'.format(line))

    def write_command(self, command):
        """Write the command using the necessary Formatter."""
        self._maybe_truncate()
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

    def _ensure_file(self, filepath):
        try:
            with open(filepath, 'r'):
                pass
        except IOError:
            with open(filepath, 'w'):
                pass
        except Exception as e:
            raise ThymeHistoryFileException(e)

    def _maybe_truncate(self):
        lines = self.readlines()
        if len(lines) < self.max_length:
            return

        with self._open_file(mode='w'):
            for line in lines[1:]:
                self.writeline(line)


class HistoryCommandEncoder(object):
    """Modular encoder for encoding and decoding commands."""

    def decode(self, line):
        """Convert command string into storable format."""
        command = line.split(':0;')[-1]
        return command

    def encode(self, command):
        """Convert store-formatted command into simple."""
        command = command.to_string()
        stamp = int(time.time())
        return ': {stamp}:0;{command}'.format(stamp=stamp, command=command)


class History(object):
    def __init__(self):
        filepath = config.get_history_filepath()
        max_lines = config.get_max_history_size()
        self.file = HistoryFile(filepath, max_lines)

    def execute(self, mode, *args, **kwargs):
        """Method used to record a command.

        We take a mode <thyme.modes.Mode> and run it's `execute` method
        after writing the command to the history file.
        """
        rv = mode.execute(*args, **kwargs)
        self.file.write_command(mode)
        return rv

    def list(self):
        """List every command in the history file."""
        history = self.file.read()
        return history

    def search(self, filter_):
        """Search history filtering on a single string."""
        history = self.file.readlines()
        filtered = [command for command in history if filter_ in command]
        return "".join(filtered)
