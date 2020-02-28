import boto3
import argparse
import re
from pscase.utils.PSCase import PSCase
from boto3.dynamodb.conditions import Attr

# DDB vars
_DDB_TABLE_NAME = 'cases'
_DDB_TABLE_NAME_TEST = 'cases-test'
_ddb_client = boto3.client('dynamodb')
_ddb_resource = boto3.resource('dynamodb')
last_case_id = _ddb_client.scan(TableName=_DDB_TABLE_NAME, Select='COUNT')['Count']

# CLI args
DATE_REGEX = '^\d{2}\/\d{2}\/\d{2}$'

# Other vars
_CASE_PATH = '$HOME/aws/cases/bigdata/'
_CASE_PATH_TEST = '$HOME/aws/cases/test/'
TEXT_EDITOR_COMMAND = 'subl'


def date_type(input_date, pattern=re.compile(DATE_REGEX)):
    """
    Defines a date type with a specific format for use in the CLI args
    :param input_date: Date to be evaluated
    :param pattern: Regular expression defining the expected date format
    :return:
    """
    if not pattern.match(input_date):
        print('Date does not match expected format.')
        raise argparse.ArgumentTypeError

    return input_date


def get_ddb_table_name(test_flag=False):
    """
    Returns the right DDB table name based on whether this is a test or not.
    :param test_flag: Boolean flag, if true return the testing table instead
    :return: DDB table name
    """
    return _DDB_TABLE_NAME_TEST if test_flag else _DDB_TABLE_NAME


def get_case_path(test_flag=False):
    """
    Returns the right case path based on whether this is a test or not.
    :param test_flag: Boolean flag, if true return to the testing path instead
    :return: Case path
    """
    return _CASE_PATH_TEST if test_flag else _CASE_PATH


def upload_case_to_ddb(case, test_flag):
    """
    Uploads a given case to the DynamoDB table
    :param case: PSCase object with the case data
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return: Result of the put_item operation
    """
    return _ddb_client.put_item(TableName=get_ddb_table_name(test_flag), Item=case.to_ddb_item())


def get_ddb_case_from_case_id(case_id):
    """
    Gets a PSCase object from DDB using a case ID
    :param case_id: Case ID of the case to retrieve
    :return: PSCase or None, depending on whether the case existed on the table
    """
    table = _ddb_resource.Table(get_ddb_table_name())
    response = table.get_item(Key={'case_id': int(case_id)})
    return PSCase.from_dictionary(response['Item']) if 'Item' in response else None


def get_ddb_case_from_number(number):
    """
    Gets a PSCase object from DDB using a case number
    :param number: Number of the case to retrieve
    :return: PSCase or None, depending on whether the case existed on the table
    """
    table = _ddb_resource.Table(get_ddb_table_name())
    results = table.scan(FilterExpression=Attr("number").eq(number))["Items"]
    return PSCase.from_dictionary(results[0]) if len(results) > 0 else None
