from ipaddress import ip_address

from common_utils.aws import get_ec2_address_by_name
from common_utils.network.ConnectionParams import ConnectionParams

bastion_params = ConnectionParams(host=get_ec2_address_by_name('bertolb'), username='ec2-user')


def build_ssh_command(address: str, username: str, pkey_path="", port=22, options=""):
    """
    Builds an SSH command to connect to an EC2 instance. If the provided address is private,
    it will add an in-between bastion instance to make the connection possible
    :param address: Address to connect to
    :param username: Username to use in the connection
    :param pkey_path: Path to the private key file to use in the connection
    :param port: SSH port
    :param options: Additional options to add to the command
    :return: SSH command
    """
    params = ConnectionParams(host=address, port=port, username=username, key=pkey_path, options=options)
    return _compose_with_bastion(params) if ip_address(address).is_private else _compose_without_bastion(params)


def _compose_with_bastion(params):
    """
    Writes an SSH command with an in-between bastion instance
    :param params: ConnectionParams object
    :return: SSH command
    """
    bastion_command = _compose_ssh_command(bastion_params)
    instance_command = _compose_ssh_command(params)
    return f'{bastion_command} {instance_command}'


def _compose_without_bastion(params):
    """
    Writes an SSH command without an in-between bastion instance
    :param params: ConnectionParams object
    :return: SSH command
    """
    return _compose_ssh_command(params)


def _compose_ssh_command(params):
    """
    Provided a ConnectionParams object, writes an SSH command with its properties
    :param params: ConnectionParams object
    :return: SSH command
    """
    command = f'ssh {params.options} {f"-i {params.key}" if params.key else ""} ' \
              f'{params.username}@{params.host} -p {params.port}'
    return " ".join(command.split())  # Remove the unnecessary spaces
