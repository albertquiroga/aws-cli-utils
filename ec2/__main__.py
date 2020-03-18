import sys
import argparse
from ec2.connect import connect_to_ec2_instance
from ec2.list import list_ec2_instances

DEFAULT_EC2_NAME = 'bertolb'
DEFAULT_USERNAME = 'ec2-user'
DEFAULT_PORT = 22

# Top-level parser
parser = argparse.ArgumentParser(prog='ec2', description='CLI tool to manage EC2 resources')
subparsers = parser.add_subparsers()

# Connect command
parser_connect = subparsers.add_parser('connect')
parser_connect.add_argument('name', type=str, nargs='?', default=DEFAULT_EC2_NAME)
parser_connect.add_argument('-k', '--key', type=str)
parser_connect.add_argument('-u', '--user', type=str, default=DEFAULT_USERNAME)
parser_connect.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
parser_connect.add_argument('-P', '--print', action='store_true', default=False,
                            help='print the SSH command instead of executing it')
parser_connect.set_defaults(func=connect_to_ec2_instance)

# List command
parser_list = subparsers.add_parser('list')
parser_list.set_defaults(func=list_ec2_instances)


def main():
    """
    Main function. Evaluates the CLI args and prints the help message if there are none
    :return: None
    """
    args = parser.parse_args()

    if not len(vars(args)) == 0:
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
