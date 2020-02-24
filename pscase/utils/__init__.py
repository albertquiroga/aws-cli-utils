import boto3
import argparse
import re

# DDB vars
_DDB_TABLE_NAME = 'cases'
_DDB_TABLE_NAME_TEST = 'cases-test'
ddb_client = boto3.client('dynamodb')
ddb_resource = boto3.resource('dynamodb')
last_case_id = ddb_client.scan(TableName=_DDB_TABLE_NAME, Select='COUNT')['Count']

# CLI args
DATE_REGEX = '^\d{2}\/\d{2}\/\d{2}$'
URL_REGEX = 'https:\/\/paragon-na\.amazon\.com\/hz\/view-case\?caseId=\d+'

# Other vars
_CASE_PATH = '$HOME/aws/cases/bigdata/'
_CASE_PATH_TEST = '$HOME/aws/cases/test/'
TEXT_EDITOR_COMMAND = 'subl'


def date_type(input_date, pattern=re.compile(DATE_REGEX)):
    if not pattern.match(input_date):
        print('Date does not match expected format.')
        raise argparse.ArgumentTypeError

    return input_date


def url_type(input_url, pattern=re.compile(URL_REGEX)):
    if not pattern.match(input_url):
        print('URL does not match expected format.')
        raise argparse.ArgumentTypeError

    return input_url


def get_ddb_table_name(test_flag=False):
    return _DDB_TABLE_NAME_TEST if test_flag else _DDB_TABLE_NAME


def get_case_path(test_flag=False):
    return _CASE_PATH_TEST if test_flag else _CASE_PATH
