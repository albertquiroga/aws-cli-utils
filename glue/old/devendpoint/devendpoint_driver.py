import os
import boto3
import argparse
from bertolb_utils import build_ssh_command

DEVENDPOINT_DEFAULT_NAME = 'bertolb-s3'
DEFAULT_USERNAME = 'glue'
PKEY_DEFAULT_PATH = '/Users/bertolb/aws/keypairs/glue/glue'
TUNNEL_ARGS = '-vnNT -L :9007:169.254.76.1:9007'

glue = boto3.client('glue')

parser = argparse.ArgumentParser(prog='devendpoint', description='Connect to Glue dev endpoints')
parser.add_argument('-n', '--name', action='store', default=DEVENDPOINT_DEFAULT_NAME, help='name of the dev endpoint to connect to')
parser.add_argument('-k', '--key', action='store', default=PKEY_DEFAULT_PATH, help='path to private SSH key to use')
parser.add_argument('-t', '--tunnel', action='store_true', default=False, help='create an SSH tunnel instead of REPL')
parser.add_argument('-p', '--print', action='store_true', default=False, help='print SSH command instead of running it')
parser.add_argument('-l', '--language', action='store', default='python', choices=['python', 'scala', 'none'], help='what REPL to launch (or none). Default: python')

cli_args_dict = vars(parser.parse_args())

language_dict = {
    'python': '-t gluepyspark',
    'scala': '-t glue-spark-shell',
    'none': ''
}


def main():
    """
    Main function. Retrieves the hostname of the specified Glue Dev Endpoint, then connects to it.
    :return: None
    """
    hostname = glue.get_dev_endpoint(EndpointName=cli_args_dict['name'])['DevEndpoint']['PublicAddress']
    command = build_ssh_command(hostname=hostname,
                                username=DEFAULT_USERNAME,
                                pkey_path=cli_args_dict['key'],
                                extra_args=TUNNEL_ARGS if cli_args_dict['tunnel'] else language_dict[cli_args_dict['language']])
    print(command) if cli_args_dict['print'] else os.system(command)
