import configparser
import re
from pathlib import Path

DEFAULT_SSH_OPTIONS = '-At -o StrictHostKeyChecking=no -o ServerAliveInterval=10'
AWS_HOSTNAME_PATTERN = r'(?:ec2|ip)-(\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}).*'
CONFIG_FILE_PATH = f'{str(Path.home())}/.aws-cli-utils'


def extract_ip_address_from_aws_hostname(aws_hostname: str) -> str:
    """
    Extracts an IP address from a provided AWS hostname using regular expression capture groups
    :param aws_hostname: AWS hostname
    :return: IP address
    """
    match = re.search(AWS_HOSTNAME_PATTERN, aws_hostname)
    return match.group(1).replace('-', '.')


def load_user_configuration_file() -> configparser.ConfigParser:
    """
    Loads the user configuration file and returns it as a ConfigParser object
    :return: ConfigParser object with the file information
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config
