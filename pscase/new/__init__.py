import os
from urllib.parse import urlparse
from pscase.utils import get_case_path, get_ddb_table_name, ddb_client, TEXT_EDITOR_COMMAND
import pyperclip


def gather_case_info(args):
    """
    Checks the contents of the args dictionary, and if there any missing information it will ask the user for it
    :param args: Args dictionary from argparse
    :return: Properly-filled args dictionary
    """
    if not args['topic']:
        args['topic'] = input("Case topic: ")

    if not args['title']:
        args['title'] = input("Case title: ")

    if not args['url']:
        args['url'] = input("Case URL: ")

    if not args['description']:
        args['description'] = input("Description: ")

    if not args['notes']:
        args['notes'] = input("Special notes: ")

    args['case_id'] = urlparse(args['url']).query.split('=')[1]

    return args


def upload_case(case_dict, test_flag):
    """
    Uploads a given case to the DynamoDB table
    :param case_dict: Dictionary containing the case information
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return: Result of the put_item operation
    """
    item = {}

    for key in case_dict.keys():
        if case_dict[key]:
            item[key] = {"N" if key == "id" else "S": case_dict[key]}

    return ddb_client.put_item(TableName=get_ddb_table_name(test_flag), Item=item)


def create_case_file(case_id, test):
    """
    Creates the case text file in the right folder
    :param case_id: Local case ID
    :param test: Boolean flag, if true create in the testing folder instead
    :return: None
    """
    os.system(f'{TEXT_EDITOR_COMMAND} {get_case_path(test)}case{case_id}.txt')


def create_new_case(args):
    print(args)
    args = vars(args)
    args.pop('func')
    test_flag = args.pop('test', None)
    case_data = gather_case_info(args)
    response = upload_case(case_data, test_flag)
    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code == 200:
        create_case_file(case_data['id'], test_flag)
        pyperclip.copy(case_data['description'])
        print(f"Case {case_data['id']} successfully created.")
    else:
        print(f'Error, HTTP status code was {str(response_code)}')
