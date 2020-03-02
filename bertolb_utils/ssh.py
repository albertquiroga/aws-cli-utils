import re
import boto3
import ipaddress


ec2 = boto3.client('ec2')

AWS_HOSTNAME_PATTERN = '(?:ec2|ip)-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}).*'
DEFAULT_SSH_OPTIONS = '-At -o StrictHostKeyChecking=no -o ServerAliveInterval=10'


class ConnectionParams:
    def __init__(self, host, username, port=22, key="", options=DEFAULT_SSH_OPTIONS):
        self.host = host
        self.port = port
        self.username = username
        self.key = key
        self.options = options


def extract_ip_address_from_aws_hostname(aws_hostname):
    match = re.search(AWS_HOSTNAME_PATTERN, aws_hostname)
    return match.group(1).replace('-', '.')


def find_ec2_instance_address_by_name(instance_name):
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}, {'Name': 'instance-state-name', 'Values': ['running']}])
    if response['Reservations']:
        instance = response['Reservations'][0]['Instances'][0]
        return instance['PublicIpAddress'] if 'PublicIpAddress' in instance else instance['PrivateIpAddress']
    else:
        return None


def _compose_ssh_command(params):
    command = f'ssh {params.options} {f"-i {params.key}" if params.key else ""} {params.username}@{params.host} -p {params.port}'
    return " ".join(command.split())  # Remove the unnecessary spaces


def _compose_with_bastion(params):
    bastion_command = _compose_ssh_command(bastion_params)
    instance_command = _compose_ssh_command(params)
    return f'{bastion_command} {instance_command}'


def _compose_without_bastion(params):
    return _compose_ssh_command(params)


bastion_params = ConnectionParams(host=find_ec2_instance_address_by_name('bertolb'), username='ec2-user')


def build_ssh_command(address, username, pkey_path="", port=22, options=""):
    connection_params = ConnectionParams(host=address, port=port, username=username, key=pkey_path, options=options)
    return _compose_with_bastion(connection_params) if ipaddress.ip_address(address).is_private else _compose_without_bastion(connection_params)
