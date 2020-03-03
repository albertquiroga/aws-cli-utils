import os
import sys
import boto3
from botocore.exceptions import ClientError
from bertolb_utils.ssh import build_ssh_command
from bertolb_utils import extract_ip_address_from_aws_hostname

glue_client = boto3.client('glue')

GLUE_ENDPOINT_USERNAME = 'glue'


def connect_to_dev_endpoint(args):
    """
    Main function. Connects to the dev endpoint specified by the user as a CLI arg
    :param args: Namespace object containing CLI args
    :return: None
    """
    endpoint_address = extract_ip_address_from_aws_hostname(_get_dev_endpoint_address(args.name))
    _handle_connection(endpoint_address, args.print)


def _get_dev_endpoint_address(dev_endpoint_name):
    """
    Fetches the IP address of a development endpoint (public if possible, private if not)
    :param dev_endpoint_name: Name of the dev endpoint
    :return: IP address of the dev endpoint (public if possible, private if not)
    """
    dev_endpoint = _get_dev_endpoint(dev_endpoint_name)
    return dev_endpoint['PublicAddress'] if 'PublicAddress' in dev_endpoint else dev_endpoint['PrivateAddress']


def _get_dev_endpoint(dev_endpoint_name):
    """
    Retrieves a dev endpoint from boto3 while handling possible error exceptions
    :param dev_endpoint_name: Name of the dev endpoint
    :return: Boto3 dict representing a dev endpoint
    """
    try:
        response = glue_client.get_dev_endpoint(EndpointName=dev_endpoint_name)
        return response['DevEndpoint']
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            print('No dev endpoint was found with that name')
            sys.exit(1)
        else:
            raise()


def _handle_connection(endpoint_address, print_flag):
    """
    Build an SSH command, then runs it or prints it depending on the print flag
    :param endpoint_address: IP address of the Glue development endpoint
    :param print_flag: If true, print the command instead of executing it
    :return: None
    """
    ssh_command = build_ssh_command(address=endpoint_address, username=GLUE_ENDPOINT_USERNAME)
    print(ssh_command) if print_flag else os.system(ssh_command)
