import argparse
from glue.crawl import crawl
from glue.connect import connect_to_dev_endpoint

DEFAULT_DEV_ENDPOINT_NAME = 's3'

# Top-level parser
parser = argparse.ArgumentParser(prog='glue', description='CLI tool to manage Glue resources')
subparsers = parser.add_subparsers()

# Connect command
parser_connect = subparsers.add_parser('connect', description='Connect to Glue development endpoints')
parser_connect.add_argument('name', type=str, nargs='?', default=DEFAULT_DEV_ENDPOINT_NAME,
                            help='Name of the dev endpoint to connect to')
parser_connect.add_argument('-k', '--key', type=str, help='Path to private key file to use for auth')
parser_connect.add_argument('-p', '--print', action='store_true', default=False,
                            help='print the SSH command instead of executing it')
parser_connect.set_defaults(func=connect_to_dev_endpoint)

# Crawl command
parser_crawl = subparsers.add_parser('crawl', description='Run a crawler')
parser_crawl.add_argument('path', type=str,
                          help='s3 path to be crawled')
parser_crawl.set_defaults(func=crawl)


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