import boto3
from bertolb_utils import extract_ip_address_from_aws_hostname

emr_client = boto3.client('emr')


def get_cluster_id_from_identifier(identifier):
    """
    Returns the corresponding Cluster ID of a provided identifier.
    :param identifier: Either a cluster name or a cluster ID
    :return: Cluster ID, or None if not found
    """
    return identifier if _this_is_cluster_id(identifier) else _find_cluster_id_by_name(identifier)


def _this_is_cluster_id(identifier):
    """
    Returns true if the provided identifier is an EMR Cluster ID
    :param identifier: Either a cluster name or a cluster ID
    :return: True if a cluster ID, false if not
    """
    return identifier.startswith('j-')


def _find_cluster_id_by_name(cluster_name):
    """
    Given a cluster name, it will return its corresponding cluster ID if it can be found
    :param cluster_name: EMR cluster name
    :return: EMR cluster ID or None
    """
    cluster_list = emr_client.list_clusters(ClusterStates=['WAITING', 'RUNNING'])['Clusters']
    filtered_list = list(filter(lambda cluster: cluster['Name'] == cluster_name, cluster_list))
    return filtered_list[0]['Id'] if len(filtered_list) > 0 else None


def find_master_node_hostname(cluster_id):
    """
    Given a cluster ID, it will return the hostname of the master node
    :param cluster_id: EMR cluster iD
    :return: Hostname of the master node
    """
    response = emr_client.describe_cluster(ClusterId=cluster_id)
    return extract_ip_address_from_aws_hostname(response['Cluster']['MasterPublicDnsName'])
