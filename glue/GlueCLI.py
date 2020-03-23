from commons.cli.CLITool import CLITool
from glue.crawl import crawl
from glue.connect import connect_to_dev_endpoint
from glue.notebook import connect_to_notebook


class GlueCLI(CLITool):

    def __init__(self):
        super(EC2CLI, self).__init__(name='glue', description='CLI tool to manage Glue resources', config_key='Glue',
                                     key_parameters=['name'])

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
parser_crawl.add_argument('path', type=str, help='s3 path to be crawled')
parser_crawl.set_defaults(func=crawl)

# Notebook command
parser_notebook = subparsers.add_parser('notebook', description='Connect to a Notebook')
parser_notebook.add_argument('name', type=str, help='Name of the notebook to connect to. Partial match allowed!')
parser_notebook.set_defaults(func=connect_to_notebook)


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
