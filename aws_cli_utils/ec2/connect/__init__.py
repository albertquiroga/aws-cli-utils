import os
from argparse import Namespace

from albertquiroga_utils.network import build_ssh_command
from albertquiroga_utils.aws import get_ec2_address_by_name, get_ec2_address_by_id


def connect_to_ec2_instance(args: Namespace):
    """
    Main function. Find EC2 instance address, builds an SSH command and runs it
    :param args: Namespace object containing CLI args
    :return: None
    """
    instance_address = _get_instance_address_from_identifier(args.identifier)
    if instance_address:
        command = build_ssh_command(address=instance_address, username=args.user, pkey_path=args.key, port=args.port)
        print(command) if args.print else os.system(command)
    else:
        print('No running EC2 instance was found with that name')


def _get_instance_address_from_identifier(idtfr: str) -> str:
    """
    Returns the corresponding address of a provided identifier. Routes to the corresponding method based on
    whether the identifier is a name tag or an EC2 instance ID
    :param idtfr: Instance identifier (name tag or instance ID)
    :return: Instance address
    """
    return get_ec2_address_by_id(idtfr) if _this_is_instance_id(idtfr) else get_ec2_address_by_name(idtfr)


def _this_is_instance_id(identifier: str) -> bool:
    """
    Returns true if the provided identifier is an EC2 instance ID
    :param identifier: Instance identifier (name tag or instance ID)
    :return: True if an instance ID, false if not
    """
    return identifier.startswith('i-')
