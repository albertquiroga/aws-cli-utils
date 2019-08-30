import boto3
import os
import argparse
import sys

emr = boto3.client('emr')
ec2 = boto3.client('ec2')

parser = argparse.ArgumentParser(prog='emr', description='Connect and manage EMR clusters')
parser.add_argument('-i', '--info', action='store_true', help='Only display cluster info')
parser.add_argument('-t', '--tunnel', action='store_true', help='Open a dynamic SSH tunnel on port 8157 instead of connecting')
parser.add_argument('-b', '--bastion', action='store_true', help='Connect to the bastion instance instead')
parser.add_argument('-n', '--node', action='store', help='Connect to the specified EC2 instance ID that is part of the cluster')

cli_args_dict = vars(parser.parse_args())


def find_cluster_id():
    cluster_list = emr.list_clusters(
        ClusterStates=['WAITING', 'RUNNING']
    )

    cluster_id_string = ''

    for cluster in cluster_list.get('Clusters', []):
        if cluster.get('Name') == 'bertolb':
            cluster_id_string = cluster.get('Id')

    return cluster_id_string


def get_master_dns_name(var_cluster_id):
    cluster_info = emr.describe_cluster(ClusterId=var_cluster_id)
    return cluster_info.get('Cluster').get('MasterPublicDnsName')


def find_instance_url(filter_name, filter_value):
    instances = ec2.describe_instances(
        Filters=[
            {
                'Name': filter_name,
                'Values': [
                    filter_value
                ]
            }
        ]
    )

    dns_name = ''

    for reservation in instances.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            dns_name = instance.get('PublicDnsName') if instance.get('PublicDnsName') else instance.get(
                'PrivateDnsName')

    return dns_name


def find_bastion_url():
    return find_instance_url('tag:Name', 'emr-bastion')


def find_node_url(instance_id):
    return find_instance_url('instance-id', instance_id)


def print_instances(instance_list):
    for instance in instance_list.get('Instances', []):
        instance_ec2_id = instance.get('Ec2InstanceId')
        private_dns_name = instance.get('PrivateDnsName')

        print('\t{:<20} {:<50}'.format(instance_ec2_id, private_dns_name))


def print_instance_group(instance_group):
    instance_group_type = instance_group.get('InstanceGroupType')
    instance_group_id = instance_group.get('Id')

    print(instance_group_type)

    instances_info = emr.list_instances(
        ClusterId=cluster_id,
        InstanceGroupId=instance_group_id
    )

    print_instances(instances_info)


cluster_id = find_cluster_id()
bastion_url = find_bastion_url()


def print_cluster_info():
    print('EMR Cluster ID:\t' + cluster_id)
    print('Bastion URL:\t' + bastion_url)

    cluster_info = emr.list_instance_groups(
        ClusterId=cluster_id
    )

    print("\nEC2 instances:")
    print('\t{:<20} {:<50}'.format("EC2 instance ID", "Private DNS hostname"))

    for instanceGroup in cluster_info.get('InstanceGroups', []):
        print_instance_group(instanceGroup)


def print_tunnel_info():
    master_dns = get_master_dns_name(cluster_id)
    print('Endpoints available:')
    print('\t{:<25} {:<50}'.format("YARN ResourceManager", "http://" + master_dns + ":8088"))
    print('\t{:<25} {:<50}'.format("HDFS NameNode", "http://" + master_dns + ":50070"))
    print('\t{:<25} {:<50}'.format("Spark HistoryServer", "http://" + master_dns + ":18080"))
    print('\t{:<25} {:<50}'.format("Zeppelin", "http://" + master_dns + ":8890"))
    print('\t{:<25} {:<50}'.format("Hue", "http://" + master_dns + ":8888"))
    print('\t{:<25} {:<50}'.format("Ganglia", "http://" + master_dns + "/ganglia"))
    print('\t{:<25} {:<50}'.format("HBase UI", "http://" + master_dns + ":16010"))


def append_string(total, new):
    return total + " " + new


def build_ssh_command(user, url, tunnel=False, bastion=False, bastion_user='', bastion_dns_name=''):
    start = 'ssh'
    bastion_options = '-At'
    default_options = '-o StrictHostKeyChecking=no -o ServerAliveInterval=10'
    tunnel_options = '-ND 8157'
    key_pair = '-i ~/aws/keypairs/bertolb-ireland.pem'

    command = ''

    command = append_string(command, start)
    if bastion:
        command = append_string(command, bastion_options)
    command = append_string(command, default_options)
    if tunnel:
        command = append_string(command, tunnel_options)
    command = append_string(command, key_pair)
    if bastion:
        command = append_string(command, bastion_user + '@' + bastion_dns_name)
        command = append_string(command, start)
        command = append_string(command, default_options)
    command = append_string(command, user + '@' + url)

    print(command)
    return command


def connect_tunnel():
    print_tunnel_info()
    os.system(build_ssh_command('ec2-user', bastion_url, tunnel=True))


def connect_bastion():
    os.system(build_ssh_command('ec2-user', bastion_url))


def connect_node(node_id):
    os.system(build_ssh_command(user='hadoop', url=find_node_url(node_id), bastion=True, bastion_user='ec2-user', bastion_dns_name=bastion_url))


def connect_master():
    os.system(build_ssh_command(user='hadoop', url=get_master_dns_name(cluster_id), bastion=True, bastion_user='ec2-user', bastion_dns_name=bastion_url))


def main():
    if cli_args_dict.get('info'):
        print_cluster_info()
        sys.exit()

    if cli_args_dict.get('tunnel'):
        connect_tunnel()
        sys.exit()

    if cli_args_dict.get('bastion'):
        connect_bastion()
        sys.exit()

    if cli_args_dict.get('node') is not None:
        connect_node(cli_args_dict.get('node'))
        sys.exit()

    connect_master()