import commands as cmd


class Thyme(object):
    def __init__(self, parser):
        self.parser = parser
        try:
            self.args = parser.parse_args()
        except Exception as e:
            print e

    def run(self):
        command = self._get_command(self.args)
        res = command.execute()
        self._handle_result(res)

    def _handle_result(self, result):
        if result:
            print(str(result))
            return

        if not result:
            print result
            for e in result.errors:
                print("%s error: %s" % (e.category, e.message))
            return

    def _get_command(sef, args):
        if args.timestamp:
            command = cmd.FromTimestampCommand(args)
        elif args.datetime:
            command = cmd.FromDatetimeCommand(args)
        else:
            command = _find_command(args)

        if not command:
            raise ValueError("Could not find a command for your query.")

        return command


def _find_command(args):
    try:
        args.datething = float(args.datething)
        return cmd.FromTimestampCommand(args)
    except ValueError:
        return cmd.FromDatetimeCommand(args)
