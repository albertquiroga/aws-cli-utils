import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

HEADERS = ['Name', 'Instance ID', 'Private IP address', 'Public IP address']


def _get_instances():
    response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(ec2_resource.Instance(instance['InstanceId']))
    return instances


def _print_row(name, instance_id, private_ip_address, public_ip_address):
    print('{:<20} {:<20} {:<20} {:<20}'.format(name, instance_id, private_ip_address, public_ip_address))


def _extract_name_from_tags(tags_list):
    name_dict = {}
    for tag in tags_list:
        if tag['Key'] == 'Name':
            name_dict = tag

    return name_dict['Value'] if name_dict else ''


def _print_instances(instances):
    _print_row(*HEADERS)
    for instance in instances:
        _print_row(_extract_name_from_tags(instance.tags), instance.id, instance.private_ip_address, instance.public_ip_address)


def list_ec2_instances(args):
    _print_instances(_get_instances())
