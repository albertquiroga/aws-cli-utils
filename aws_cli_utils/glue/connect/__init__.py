import os
import sys
import argparse
from typing import Union

from aws_cli_utils.common_utils.aws import glue_client

from albertquiroga_utils.network import build_ssh_command
from albertquiroga_utils.aws import extract_ip_address_from_aws_hostname
from botocore.exceptions import ClientError

GLUE_ENDPOINT_USERNAME = 'glue'


def connect_to_dev_endpoint(args: argparse.Namespace):
    """
    Main function. Connects to the dev endpoint specified by the user as a CLI arg
    :param args: Namespace object containing CLI args
    :return: None
    """
    endpoint_address = extract_ip_address_from_aws_hostname(_get_dev_endpoint_address(args.name))
    _handle_connection(endpoint_address, args.print)


def _get_dev_endpoint_address(dev_endpoint_name: str) -> str:
    """
    Fetches the IP address of a development endpoint (public if possible, private if not)
    :param dev_endpoint_name: Name of the dev endpoint
    :return: IP address of the dev endpoint (public if possible, private if not)
    """
    dev_endpoint = _get_dev_endpoint(dev_endpoint_name)
    return dev_endpoint['PublicAddress'] if 'PublicAddress' in dev_endpoint else dev_endpoint['PrivateAddress']


def _get_dev_endpoint(dev_endpoint_name: str) -> Union[str, None]:
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


def _handle_connection(endpoint_address: str, print_flag: bool):
    """
    Build an SSH command, then runs it or prints it depending on the print flag
    :param endpoint_address: IP address of the Glue development endpoint
    :param print_flag: If true, print the command instead of executing it
    :return: None
    """
    ssh_command = build_ssh_command(address=endpoint_address, username=GLUE_ENDPOINT_USERNAME)
    print(ssh_command) if print_flag else os.system(ssh_command)
