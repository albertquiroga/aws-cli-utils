import configparser
from pathlib import Path

DEFAULT_SSH_OPTIONS = '-At -o StrictHostKeyChecking=no -o ServerAliveInterval=10'
CONFIG_FILE_PATH = f'{str(Path.home())}/.aws-cli-utils'


def load_user_configuration_file() -> configparser.ConfigParser:
    """
    Loads the user configuration file and returns it as a ConfigParser object
    :return: ConfigParser object with the file information
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config


def divide_chunks(big_list: list, chunk_size: int) -> list:
    """
    Divides a list into equal chunks of size 'chunk_size'
    :param big_list: List to be divided
    :param chunk_size: Number of items per chunk
    :return: List of lists
    """
    for i in range(0, len(big_list), chunk_size):
        yield big_list[i:i + chunk_size]
