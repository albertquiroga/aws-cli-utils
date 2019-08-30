import boto3
import argparse
import os
from bertolb_utils import build_ssh_command

DEFAULT_EC2_NAME = 'bertolb'
DEFAULT_USERNAME = 'ec2-user'
DEFAULT_PKEY_PATH = '~/aws/keypairs/bertolb-ireland.pem'

ec2 = boto3.client('ec2')

parser = argparse.ArgumentParser(prog='ec2', description='Connect and manage EC2 instances')
parser.add_argument('-n', '--name', action='store', default=DEFAULT_EC2_NAME, help='connect to the specified EC2 instance name (tag:Name)')
parser.add_argument('-u', '--user', action='store', default=DEFAULT_USERNAME, help='username to use in the login')
parser.add_argument('-k', '--key', action='store', default=DEFAULT_PKEY_PATH, help='path to private SSH key to use')

cli_args_dict = vars(parser.parse_args())


def find_instance_url(instance_name):
    """
    Finds an EC2 instance with the 'Name' tag value equal to the one passed as parameter
    :param instance_name: Value for the 'Name' tag of the EC2 instance
    :return: Hostname of the instance.
    """
    instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])

    hostname = ''

    for reservation in instances.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            hostname = instance.get('PublicDnsName') if instance.get('PublicDnsName') else instance.get('PrivateDnsName')

    return hostname


def main():
    """
    Main function. Tries to find an EC2 instance with the provided name. If it can't, prints error message. If it
    can, builds the SSH command to connect to it and runs it.
    :return: Exit code
    """
    instance_url = find_instance_url(cli_args_dict['name'])
    if instance_url:
        os.system(build_ssh_command(hostname=instance_url,
                                    username=cli_args_dict['user'],
                                    pkey_path=cli_args_dict['key']))
    else:
        print('No EC2 instance with that name was found')
