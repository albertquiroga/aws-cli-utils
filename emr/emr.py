import argparse
from emr.connect import connect_to_emr_cluster
from emr.info import print_emr_cluster_info

DEFAULT_CLUSTER_NAME = 'bertolb'

# Top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Connect command
parser_connect = subparsers.add_parser('connect')
parser_connect.add_argument('identifier', type=str, nargs='?', default=DEFAULT_CLUSTER_NAME,
                            help='Identifier of the cluster to connect to. This can either be a cluster ID or a '
                                 '"Name" tag')
parser_connect.add_argument('-k', '--key', type=str, help='Path to private key file to use for auth')
parser_connect.add_argument('-p', '--print', action='store_true', default=False,
                            help='print the SSH command instead of executing it')
parser_connect.set_defaults(func=connect_to_emr_cluster)

# Info command
parser_info = subparsers.add_parser('info')
parser_info.add_argument('identifier', type=str, nargs='?', default=DEFAULT_CLUSTER_NAME,
                         help='Identifier of the cluster to connect to. This can either be a cluster ID or a '
                              '"Name" tag')
parser_info.set_defaults(func=print_emr_cluster_info)


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
