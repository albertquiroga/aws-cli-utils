from commons.cli.CLITool import CLITool
from ec2.list import list_ec2_instances
from ec2.connect import connect_to_ec2_instance

DEFAULT_USERNAME = 'ec2-user'
DEFAULT_PORT = 22


class EC2CLI(CLITool):

    def __init__(self):
        super(EC2CLI, self).__init__(name='ec2', description='CLI tool to manage EC2 resources', config_key='EC2',
                                     key_parameters=['name'])

        subparsers = self.parser.add_subparsers()

        # Connect command
        parser_connect = subparsers.add_parser('connect')
        parser_connect.add_argument('name', type=str, nargs='?', default=self.config.get('DefaultInstanceName', ''))
        parser_connect.add_argument('-k', '--key', type=str)
        parser_connect.add_argument('-u', '--user', type=str,
                                    default=self.config.get('DefaultUsername', DEFAULT_USERNAME))
        parser_connect.add_argument('-p', '--port', type=int, default=self.config.get('DefaultPort', DEFAULT_PORT))
        parser_connect.add_argument('-P', '--print', action='store_true', default=False,
                                    help='print the SSH command instead of executing it')
        parser_connect.set_defaults(func=connect_to_ec2_instance)

        # List command
        parser_list = subparsers.add_parser('list')
        parser_list.set_defaults(func=list_ec2_instances)
