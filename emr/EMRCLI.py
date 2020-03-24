from commons.cli.CLITool import CLITool
from emr.connect import connect_to_emr_cluster
from emr.info import print_emr_cluster_info


class EMRCLI(CLITool):

    def __init__(self):
        super(EMRCLI, self).__init__(name='emr', description='CLI tool to manage EMR resources', config_key='EMR',
                                     key_parameters={'connect': ['identifier'], 'info': ['identifier']})

        # Connect command
        parser_connect = self.subparsers.add_parser(name='connect', description='Connect to EMR cluster via SSH')
        parser_connect.add_argument('identifier', type=str, nargs='?',
                                    default=self.config.get('DefaultClusterIdentifier', ''),
                                    help='Identifier of the cluster to connect to. This can either be a cluster ID or '
                                         'a "Name" tag')
        parser_connect.add_argument('-k', '--key', type=str, help='Path to private key file to use for auth')
        parser_connect.add_argument('-p', '--print', action='store_true', default=False,
                                    help='print the SSH command instead of executing it')
        parser_connect.set_defaults(func=connect_to_emr_cluster)

        # Info command
        parser_info = self.subparsers.add_parser(name='info', description='Print information about an EMR cluster')
        parser_info.add_argument('identifier', type=str, nargs='?',
                                 default=self.config.get('DefaultClusterIdentifier', ''),
                                 help='Identifier of the cluster to connect to. This can either be a cluster ID or a '
                                      '"Name" tag')
        parser_info.set_defaults(func=print_emr_cluster_info)
