import re
from typing import Union

import boto3

AWS_HOSTNAME_PATTERN = r'(?:ec2|ip)-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}).*'

ec2 = boto3.client('ec2')


def get_ec2_address_by_name(instance_name: str) -> Union[str, None]:
    """
    Returns an instance's IP address (public if possible, private if not) based on its 'Name' tag
    :param instance_name: 'Name' tag of the instance
    :return: IP address of the instance (public if possible, private if not)
    """
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]},
                                               {'Name': 'instance-state-name', 'Values': ['running']}])
    return _get_address_from_instance_response(response)


def get_ec2_address_by_id(instance_id: str) -> Union[str, None]:
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return _get_address_from_instance_response(response)


def _get_address_from_instance_response(instance_response: dict) -> Union[str, None]:
    if instance_response['Reservations']:
        instance = instance_response['Reservations'][0]['Instances'][0]
        return instance['PublicIpAddress'] if 'PublicIpAddress' in instance else instance['PrivateIpAddress']
    else:
        return None


def extract_ip_address_from_aws_hostname(aws_hostname: str) -> str:
    """
    Extracts an IP address from a provided AWS hostname using regular expression capture groups
    :param aws_hostname: AWS hostname
    :return: IP address
    """
    match = re.search(AWS_HOSTNAME_PATTERN, aws_hostname)
    return match.group(1).replace('-', '.')
