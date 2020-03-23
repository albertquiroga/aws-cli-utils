import os
import sys
from commons.ssh import build_ssh_command
from emr.utils import get_cluster_id_from_identifier, find_master_node_hostname


def connect_to_emr_cluster(args):
    """
    Main function. Retrieves the cluster ID, builds an SSH command to connect to it and
    then either runs it or prints it depending on the configuration
    :param args: Namespace object containing CLI args
    :return: None
    """
    cluster_id = get_cluster_id_from_identifier(args.identifier)
    if cluster_id:
        _handle_connection(address=find_master_node_hostname(cluster_id), key=args.key, print_flag=args.print)
    else:
        _exit_because_no_cluster_found()


def _exit_because_no_cluster_found():
    """
    If no cluster has been found for that identifier, inform the user and exit
    :return: None
    """
    print('No running cluster was found with that name')
    sys.exit(1)


def _handle_connection(address, key, print_flag):
    """
    Build an SSH command, then runs it or prints it depending on the print flag
    :param address: Address of the node to connect to
    :param key: Path to private key file to use in the connection
    :param print_flag: If true, print the command instead of executing it
    :return: None
    """
    ssh_command = build_ssh_command(address=address, username='hadoop', pkey_path=key)
    os.system(ssh_command) if not print_flag else print(ssh_command)
