import os
import boto3
import argparse
import pyperclip
from datetime import date

from cases.data_gather import gather_case_info

# DDB vars
DDB_TABLE_NAME = 'cases'
ddb = boto3.client('dynamodb')
last_case_id = ddb.scan(TableName=DDB_TABLE_NAME, Select='COUNT')['Count']

# CLI args
parser = argparse.ArgumentParser(prog='awscase', description='Manage AWS PS cases')
parser.add_argument('--id', action='store', default=str(last_case_id + 1), help='Local case number')
parser.add_argument('--date', action='store', default=date.today().strftime("%m/%d/%y"), help='Date in mm/dd/yy format')
parser.add_argument('--url', action='store', help='Case URL')
parser.add_argument('--title', action='store', help='Case title')
parser.add_argument('--topic', action='store', help='Case topic')
parser.add_argument('--description', action='store', help='Description about the issue')
parser.add_argument('--notes', action='store', help='Any other notes')
cli_args_dict = vars(parser.parse_args())

# Case vars
CASE_PATH = '$HOME/aws/cases/bigdata/'


def get_new_case_id():
    return ddb.scan(TableName=DDB_TABLE_NAME, Select='COUNT')['Count'] + 1


def upload_case(case_dict):
    item = {}

    for key in case_dict.keys():
        if case_dict[key]:
            item[key] = {"N" if key == "id" else "S": case_dict[key]}

    return ddb.put_item(TableName=DDB_TABLE_NAME, Item=item)


def create_case_file(case_id):
    os.system(f'subl {CASE_PATH}case{case_id}.txt')  # TODO add support for more editors


def main():
    case_data = gather_case_info(cli_args_dict)
    response = upload_case(case_data)
    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code == 200:
        create_case_file(case_data['id'])
        pyperclip.copy(case_data['description'])
        print(f"Case {case_data['id']} successfully created.")
    else:
        print(f'Error, HTTP status code was {str(response_code)}')
