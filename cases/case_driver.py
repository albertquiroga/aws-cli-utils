import os
import boto3
import argparse
import pyperclip
import re
from datetime import date

from cases.data_gather import gather_case_info

# DDB vars
DDB_TABLE_NAME = 'cases'
DDB_TABLE_NAME_TEST = 'cases-test'
ddb = boto3.client('dynamodb')
last_case_id = ddb.scan(TableName=DDB_TABLE_NAME, Select='COUNT')['Count']

# CLI args
DATE_REGEX = '^\d{2}\/\d{2}\/\d{2}$'
URL_REGEX = 'https:\/\/paragon-na\.amazon\.com\/hz\/view-case\?caseId=\d+'


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


parser = argparse.ArgumentParser(prog='awscase', description='Manage AWS PS cases')
parser.add_argument('--id', action='store', default=str(last_case_id + 1), help='Local case number')
parser.add_argument('--date', action='store', type=date_type, default=date.today().strftime("%m/%d/%y"), help='Date in mm/dd/yy format')
parser.add_argument('--url', action='store', type=url_type, help='Case URL')
parser.add_argument('--title', action='store', help='Case title')
parser.add_argument('--topic', action='store', help='Case topic')
parser.add_argument('--description', action='store', help='Description about the issue')
parser.add_argument('--notes', action='store', help='Any other notes')
parser.add_argument('--test', action='store_true', help='Write to test DDB table and path instead')
cli_args_dict = vars(parser.parse_args())

# Case vars
CASE_PATH = '$HOME/aws/cases/bigdata/'
CASE_PATH_TEST = '$HOME/aws/cases/test/'


def get_new_case_id():
    return ddb.scan(TableName=DDB_TABLE_NAME, Select='COUNT')['Count'] + 1


def upload_case(case_dict, test):
    item = {}

    for key in case_dict.keys():
        if case_dict[key]:
            item[key] = {"N" if key == "id" else "S": case_dict[key]}

    table_name = DDB_TABLE_NAME_TEST if test else DDB_TABLE_NAME
    print(table_name)
    return ddb.put_item(TableName=table_name, Item=item)


def create_case_file(case_id, test):
    os.system(f'subl {CASE_PATH_TEST if test else CASE_PATH}case{case_id}.txt')  # TODO add support for more editors


def main():
    test_flag = cli_args_dict.pop('test', None)
    case_data = gather_case_info(cli_args_dict)
    response = upload_case(case_data, test_flag)
    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code == 200:
        create_case_file(case_data['id'], test_flag)
        pyperclip.copy(case_data['description'])
        print(f"Case {case_data['id']} successfully created.")
    else:
        print(f'Error, HTTP status code was {str(response_code)}')
