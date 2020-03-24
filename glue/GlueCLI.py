from commons.cli.CLITool import CLITool
from glue.crawl import crawl
from glue.connect import connect_to_dev_endpoint
from glue.notebook import connect_to_notebook


class GlueCLI(CLITool):

    def __init__(self):
        super(GlueCLI, self).__init__(name='glue', description='CLI tool to manage Glue resources', config_key='Glue',
                                      key_parameters={'connect': ['name'], 'crawl': ['path'], 'notebook': ['name']})

        # Connect command
        parser_connect = self.subparsers.add_parser('connect', description='Connect to Glue development endpoints')
        parser_connect.add_argument('name', type=str, nargs='?', default=self.config.get('DefaultDevEndpointName', ''),
                                    help='Name of the dev endpoint to connect to')
        parser_connect.add_argument('-k', '--key', type=str, help='Path to private key file to use for auth')
        parser_connect.add_argument('-p', '--print', action='store_true', default=False,
                                    help='print the SSH command instead of executing it')
        parser_connect.set_defaults(func=connect_to_dev_endpoint)

        # Crawl command
        parser_crawl = self.subparsers.add_parser('crawl', description='Run a crawler')
        parser_crawl.add_argument('path', type=str, help='s3 path to be crawled')
        parser_crawl.set_defaults(func=crawl)

        # Notebook command
        parser_notebook = self.subparsers.add_parser(name='notebook', description='Connect to a SageMaker Notebook '
                                                                                  'attached to a Dev Endpoint')
        parser_notebook.add_argument('name', type=str, nargs='?', default=self.config.get('DefaultNotebookName', ''),
                                     help='Name of the notebook to connect to. Partial match allowed!')
        parser_notebook.set_defaults(func=connect_to_notebook)
