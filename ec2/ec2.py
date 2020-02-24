import argparse
from ec2.connect import connect_to_ec2_instance
from ec2.list import list_ec2_instances

DEFAULT_EC2_NAME = 'bertolb'
DEFAULT_USERNAME = 'ec2-user'
DEFAULT_PORT = 22
DEFAULT_DEV_ENDPOINT_NAME = 's3'

# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# create the parser for the "connect" command
parser_connect = subparsers.add_parser('connect')
parser_connect.add_argument('name', type=str, nargs='?', default=DEFAULT_EC2_NAME)
parser_connect.add_argument('-k', '--key', type=str)
parser_connect.add_argument('-u', '--user', type=str, default=DEFAULT_USERNAME)
parser_connect.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
parser_connect.add_argument('-P', '--print', action='store_true', default=False, help='print the SSH command instead of executing it')
parser_connect.set_defaults(func=connect_to_ec2_instance)

# create the parser for the "list" command
parser_list = subparsers.add_parser('list')
parser_list.set_defaults(func=list_ec2_instances)


def main():
    args = parser.parse_args()

    if not len(vars(args)) == 0:
        args.func(args)
    else:
        parser.print_help()
