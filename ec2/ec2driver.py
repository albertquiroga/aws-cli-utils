import boto3
import argparse
import os

ec2 = boto3.client('ec2')

parser = argparse.ArgumentParser(prog='ec2', description='Connect and manage EC2 instances')
parser.add_argument('-n', '--name', action='store', default='bertolb', help='Connect to the specified EC2 instance name (tag:Name)')
parser.add_argument('-u', '--user', action='store', default='ec2-user', help='Username to use in the login')
parser.add_argument('-k', '--keypair', action='store', default='~/aws/keypairs/bertolb-ireland.pem', help='Path to SSH keypair to use')

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


def build_ssh_command(instance_dns_name):
    """
    Builds the CLI SSH command based on the CLI arguments
    :param instance_dns_name: EC2 instance hostname
    :return: Command string
    """
    return 'ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=10 -i ' + cli_args_dict['keypair'] + ' ' + cli_args_dict['user'] + '@' + instance_dns_name


def print_no_instance_found_error():
    """
    In case we can't find any EC2 instances with the 'Name' tag equal to the provided name, print error message
    :return: None
    """
    print('No EC2 instance with that name was found')


def main():
    """
    Main function. Tries to find an EC2 instance with the provided name. If it can't, prints error message. If it
    can, builds the SSH command to connect to it and runs it.
    :return: Exit code
    """
    instance_url = find_instance_url(cli_args_dict['name'])
    os.system(build_ssh_command(instance_url)) if instance_url else print_no_instance_found_error()
