from pscase.utils import TEXT_EDITOR_COMMAND, get_case_path, ddb_resource, get_ddb_table_name
from boto3.dynamodb.conditions import Attr
import os
import sys


def _exit_because_no_case_found():
    """
    Print an error message and exit if no matching case was found in the DDB table
    :return:
    """
    print('Case not found in DDB table')
    sys.exit(1)


def _open_case_file(case):
    """
    Opens a given case's text file
    :param case: Dictionary containing the case data
    :return: None
    """
    print(f'Opening case {case["case_id"]}')
    os.system(f'{TEXT_EDITOR_COMMAND} {get_case_path()}case{case["id"]}.txt')


def open_case(args):
    case_id = args.id
    table = ddb_resource.Table(get_ddb_table_name())
    results = table.scan(FilterExpression=Attr("case_id").eq(case_id))["Items"]
    _exit_because_no_case_found() if not results else _open_case_file(results[0])
