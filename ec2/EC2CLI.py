from commons.cli.CLITool import CLITool
from ec2.list import list_ec2_instances
from ec2.connect import connect_to_ec2_instance

DEFAULT_USERNAME = 'ec2-user'
DEFAULT_PORT = 22


class EC2CLI(CLITool):

    def __init__(self):
        super(EC2CLI, self).__init__(name='ec2', description='CLI tool to manage EC2 resources', config_key='EC2',
                                     key_parameters={'connect': ['name']})

        # Connect command
        parser_connect = self.subparsers.add_parser(name='connect', description='Connect to an EC2 instance via SSH')
        parser_connect.add_argument('name', type=str, nargs='?', default=self.config.get('DefaultInstanceName', ''),
                                    help='Name tag of the EC2 instance to connect to')
        parser_connect.add_argument('-k', '--key', type=str, help='Path to private key file to use for authentication')
        parser_connect.add_argument('-u', '--user', type=str,
                                    default=self.config.get('DefaultUsername', DEFAULT_USERNAME),
                                    help='Username to be used in the connection')
        parser_connect.add_argument('-p', '--port', type=int, default=self.config.get('DefaultPort', DEFAULT_PORT),
                                    help='Port to connect to')
        parser_connect.add_argument('-P', '--print', action='store_true', default=False,
                                    help='print the SSH command instead of executing it')
        parser_connect.set_defaults(func=connect_to_ec2_instance)

        # List command
        parser_list = self.subparsers.add_parser(name='list', description='List all EC2 instances')
        parser_list.set_defaults(func=list_ec2_instances)
