import re

DEFAULT_SSH_OPTIONS = '-At -o StrictHostKeyChecking=no -o ServerAliveInterval=10'
AWS_HOSTNAME_PATTERN = r'(?:ec2|ip)-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}).*'


def extract_ip_address_from_aws_hostname(aws_hostname):
    """
    Extracts an IP address from a provided AWS hostname using regular expression capture groups
    :param aws_hostname: AWS hostname
    :return: IP address
    """
    match = re.search(AWS_HOSTNAME_PATTERN, aws_hostname)
    return match.group(1).replace('-', '.')
