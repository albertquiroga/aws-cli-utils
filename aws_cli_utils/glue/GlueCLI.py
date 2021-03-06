from aws_cli_utils.glue.crawl import crawl
from aws_cli_utils.glue.connect import connect_to_dev_endpoint
from aws_cli_utils.glue.notebook import connect_to_notebook
from aws_cli_utils.glue.dtfc import delete_tables_from_crawler

from albertquiroga_utils.cli.CLITool import CLITool

DEFAULT_CRAWLER_DATABASE_NAME = 'test'


class GlueCLI(CLITool):

    def __init__(self):
        super(GlueCLI, self).__init__(name='glue', description='CLI tool to manage Glue resources',
                                      config_section='Glue', key_parameters={'connect': ['name'],
                                                                             'crawl': ['path'],
                                                                             'notebook': ['name'],
                                                                             'dtfc': ['name']})

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
        parser_crawl.add_argument('-d', '--database', type=str,
                                  default=self.config.get('DefaultCrawlerDatabase', DEFAULT_CRAWLER_DATABASE_NAME),
                                  help='database where the resulting table will be written')
        parser_crawl.set_defaults(func=crawl)

        # Notebook command
        parser_notebook = self.subparsers.add_parser(name='notebook', description='Connect to a SageMaker Notebook '
                                                                                  'attached to a Dev Endpoint')
        parser_notebook.add_argument('name', type=str, nargs='?', default=self.config.get('DefaultNotebookName', ''),
                                     help='Name of the notebook to connect to. Partial match allowed!')
        parser_notebook.set_defaults(func=connect_to_notebook)

        # Delete tables from crawler command
        parser_dtfc = self.subparsers.add_parser(name='dtfc', description='Delete all tables created '
                                                                          'by a particular crawler')
        parser_dtfc.add_argument('name', type=str, help='Name of the crawler that created the tables')
        parser_dtfc.set_defaults(func=delete_tables_from_crawler)
