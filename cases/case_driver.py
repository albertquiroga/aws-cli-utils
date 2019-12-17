import os
import boto3
from data_gather import gather_case_info

DDB_TABLE_NAME = 'cases'
ddb = boto3.client('dynamodb')

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
    os.system('subl ' + CASE_PATH + 'case%s.txt' % case_id)  # TODO add support for more editors


def main():
    case_data = gather_case_info(get_new_case_id())
    response = upload_case(case_data)
    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code == 200:
        create_case_file(case_data['id'])
        print("Case %s successfully created." % (case_data['id']))
    else:
        print('Error, HTTP status code was ' + str(response_code))
