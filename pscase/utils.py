import boto3
import argparse
import re

# DDB vars
DDB_TABLE_NAME = 'cases'
DDB_TABLE_NAME_TEST = 'cases-test'
ddb_client = boto3.client('dynamodb')
ddb_resource = boto3.resource('dynamodb')
last_case_id = ddb_client.scan(TableName=DDB_TABLE_NAME, Select='COUNT')['Count']

# CLI args
DATE_REGEX = '^\d{2}\/\d{2}\/\d{2}$'
URL_REGEX = 'https:\/\/paragon-na\.amazon\.com\/hz\/view-case\?caseId=\d+'

# Other vars
CASE_PATH = '$HOME/aws/cases/bigdata/'
CASE_PATH_TEST = '$HOME/aws/cases/test/'
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
