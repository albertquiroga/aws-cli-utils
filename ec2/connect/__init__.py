import os
from argparse import Namespace

from commons.ssh import build_ssh_command, find_ec2_instance_address_by_name


def connect_to_ec2_instance(args: Namespace):
    """
    Main function. Find EC2 instance address, builds an SSH command and runs it
    :param args: Namespace object containing CLI args
    :return: None
    """
    instance_address = find_ec2_instance_address_by_name(args.name)
    if instance_address:
        command = build_ssh_command(address=instance_address, username=args.user, pkey_path=args.key, port=args.port)
        print(command) if args.print else os.system(command)
    else:
        print('No running EC2 instance was found with that name')
