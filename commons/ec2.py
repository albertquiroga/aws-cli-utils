from typing import Union

import boto3

ec2 = boto3.client('ec2')


def find_ec2_instance_address_by_name(instance_name: str) -> Union[str, None]:
    """
    Returns an instance's IP address (public if possible, private if not) based on its 'Name' tag
    :param instance_name: 'Name' tag of the instance
    :return: IP address of the instance (public if possible, private if not)
    """
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]},
                                               {'Name': 'instance-state-name', 'Values': ['running']}])
    if response['Reservations']:
        instance = response['Reservations'][0]['Instances'][0]
        return instance['PublicIpAddress'] if 'PublicIpAddress' in instance else instance['PrivateIpAddress']
    else:
        return None
