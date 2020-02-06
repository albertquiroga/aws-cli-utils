from pscase.utils import *
from boto3.dynamodb.conditions import Attr
import os
import sys


def exit_because_no_case_found():
    """
    Print an error message and exit if no matching case was found in the DDB table
    :return:
    """
    print('Case not found in DDB table')
    sys.exit(1)


def open_case(case):
    """
    Opens a given case's text file
    :param case: Dictionary containing the case data
    :return: None
    """
    print(f'Opening case {case["id"]}')
    os.system(f'{TEXT_EDITOR_COMMAND} {CASE_PATH}case{case["id"]}.txt')


def main(args):
    case_id = args['id']
    table = ddb_resource.Table(DDB_TABLE_NAME)
    results = table.scan(FilterExpression=Attr("case_id").eq(case_id))["Items"]
    exit_because_no_case_found() if not results else open_case(results[0])