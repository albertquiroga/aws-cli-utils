import os
import sys
from typing import Union
from argparse import Namespace

from aws_cli_utils.common_utils.aws import sagemaker_client


def connect_to_notebook(args: Namespace):
    """
    Retrieves a SageMaker notebook and connects to it. If no instance was found, prints error message and exits
    :param args: Namespace object containing CLI args
    :return: None
    """
    notebook = _get_sagemaker_instance(args.name)
    _open_notebook(notebook) if notebook else _exit_because_no_notebook_found()


def _get_sagemaker_instance(notebook_name: str) -> Union[dict, None]:
    """
    Retrieves the first SageMaker instance that contains the provided notebook name
    :param notebook_name: Name of the notebook instance. Partial match allowed
    :return: SageMaker instance boto3 object
    """
    instances = sagemaker_client.list_notebook_instances(NameContains=notebook_name)['NotebookInstances']
    return instances[0] if len(instances) > 0 else None


def _open_notebook(notebook: dict):
    """
    Informs the user and opens the URL of the provided notebook instance
    :param notebook: SageMaker instance boto3 object
    :return: None
    """
    print(f'Connecting to notebook {notebook["NotebookInstanceName"]}')
    os.system(f'open https://{notebook["Url"]}')


def _exit_because_no_notebook_found():
    """
    If no notebook instance was found with the provided name, inform the user and exit gracefully
    :return: None
    """
    print('No notebook was found with that name')
    sys.exit(1)
