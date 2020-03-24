from functools import reduce

import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

TABLE_HEADERS = ['Name', 'Instance ID', 'Private IP address', 'Public IP address']


# noinspection PyUnusedLocal
def list_ec2_instances(args):
    """
    Prints all EC2 instances in a tabular fashion
    :return: None
    """
    _print_instances(_get_instances())


def _get_instances():
    """
    Retrieves all EC2 instances in RUNNING status
    :return: List of Instance objects
    """
    response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return _process_ec2_response(response)


def _process_ec2_response(response):
    """
    Turns the AWS response dict into boto3 instance objects
    :param response: AWS response dict
    :return: List of Instance objects
    """
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(ec2_resource.Instance(instance['InstanceId']))
    return instances


def _print_instances(instances):
    """
    Takes a list of Instance objects and prints it in a tabular fashion
    :param instances: List of Instance objects
    :return: None
    """
    _print_row(*TABLE_HEADERS)
    for instance in instances:
        _print_row(_extract_name_from_tags(instance.tags), instance.id,
                   instance.private_ip_address, instance.public_ip_address)


def _print_row(name, instance_id, private_ip_address, public_ip_address):
    """
    Prints a row of EC2 instance data in a tabular fashion
    :param name: EC2 instance name
    :param instance_id: EC2 instance ID
    :param private_ip_address: Private IP address
    :param public_ip_address: Public IP address
    :return: None
    """
    print('{:<20} {:<20} {:<20} {:<20}'.format(name, instance_id, private_ip_address, public_ip_address))


def _extract_name_from_tags(tag_list):
    """
    Extracts the value of the 'Name' tag of an EC2 instance. Filters all tag dictionaries to get the one where the key
    is 'Name', then extracts the value from it. If there's several 'Name' tags, it uses the first one always
    :param tag_list: List of tags for an EC2 instance
    :return: Name value
    """
    filtered_tag_list = list(filter(lambda tag: tag['Key'] == 'Name', tag_list))
    names = list(map(lambda tag: tag['Value'], filtered_tag_list))
    return reduce(lambda a, b: a, names) if len(names) > 0 else ''
