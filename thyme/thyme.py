from parser import parser
from arg_handler import Thyme

handler = Thyme(parser)


if __name__ == '__main__':
	handler.run()