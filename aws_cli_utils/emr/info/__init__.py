from argparse import Namespace

from aws_cli_utils.emr.utils import get_cluster_id_from_identifier
from aws_cli_utils.common_utils.aws import emr_client


def print_emr_cluster_info(args: Namespace):
    """
    Main function. Retrieves the cluster ID and then prints all information regarding it
    :param args: Namespace object containing CLI args
    :return: None
    """
    cluster_id = get_cluster_id_from_identifier(args.identifier)
    _print_cluster_info(cluster_id)


def _print_cluster_info(cluster_id: str):
    """
    Prints all information of a given cluster ID
    :param cluster_id: EMR cluster ID
    :return: None
    """
    print('EMR Cluster ID:\t' + cluster_id)

    cluster_info = emr_client.list_instance_groups(ClusterId=cluster_id)

    print("\nEC2 instances:")
    print('\t{:<20} {:<20} {:<20}'.format("EC2 instance ID", "Private address", "Public address"))

    for instance_group in cluster_info['InstanceGroups']:
        _print_instance_group(instance_group, cluster_id)


def _print_instance_group(instance_group: dict, cluster_id: str):
    """
    Prints all information of a given instance group
    :param instance_group: Instance group dict
    :param cluster_id: EMR cluster ID
    :return: None
    """
    instance_group_type = instance_group['InstanceGroupType']
    instance_group_id = instance_group['Id']

    print(instance_group_type)

    instances_info = emr_client.list_instances(ClusterId=cluster_id, InstanceGroupId=instance_group_id)
    _print_instances(instances_info['Instances'])


def _print_instances(instance_list: list):
    """
    Prints all instances in an instance group
    :param instance_list: List of EC2 instances in an instance group
    :return: None
    """
    for instance in instance_list:
        print('\t{:<20} {:<20} {:<20}'.format(
            instance['Ec2InstanceId'],
            instance['PrivateIpAddress'],
            instance['PublicIpAddress'] if 'PublicIpAddress' in instance else '')
        )
