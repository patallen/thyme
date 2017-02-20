from datetime import date as d

from utils import convert_fmt

from lol import lolololololololololololololololololol
import uuid
import math
import random


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def _maybe_upper(letter):
    rand = math.floor(random.random() * 2)
    if rand and letter.isalpha():
        return letter.upper()

    return letter


def _gen_secret(length):
    alphabet = ALPHABET + '123456789!@#$%^&*()/\\~-=[]{}'
    return _random_string(length, alphabet)


def _random_string(length, alphabet=ALPHABET):
    alpha_len = len(alphabet)
    string = ""
    for _ in range(alpha_len):
        letter = alphabet[int(math.floor(random.random() * alpha_len))]
        if int(math.floor(random.random() * 2)):
            letter = _maybe_upper(letter)
        string += letter
    return string


class Command(object):
    """Base Command class. Do not instantiate."""
    COMMAND_STRING = None

    def __init__(self, args):
        self.args = args
        self.invalid_result = InvalidResult()

    def execute(self):
        raise NotImplementedError


class RandomThingCommand(Command):
    def execute(self):
        thing = self._get_thing_by_string(self.args.datething)
        return thing

    def _get_thing_by_string(self, thing):
        if thing in ('uuid', 'uid', 'guid', 'uuid4',):
            result = str(uuid.uuid4())
        elif thing in ('int', 'num', 'number',):
            result = math.ceil(random.random() * 100)
        elif thing in ('secret', 'secret_key',):
            result = _gen_secret(64)
        elif thing in ('string', 'str'):
            return _random_string(32)
        if result:
            return ValidResult(result)


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
