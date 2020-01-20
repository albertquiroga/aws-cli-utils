import boto3
import argparse

parser = argparse.ArgumentParser(prog='import_cases', description='Import AWS PS cases into a DDB table')
parser.add_argument('-f', '--file', action='store', default='/Users/bertolb/Downloads/cases.txt', help='Cases file in TSV format')
parser.add_argument('-t', '--table', action='store', default='cases', help='Name of the DDB table')
cli_args_dict = vars(parser.parse_args())

case_file = open(cli_args_dict['file'], 'r')
ddb = boto3.client('dynamodb')
separator = '\t'

# read headers
headers = case_file.readline().decode("utf-8-sig").encode("utf-8").strip().lower().strip().split(separator)
print(headers)


def process_line(line_to_process):
    d = dict(zip(headers, line_to_process))

    item = {}

    for key in d.keys():
        if d[key]:
            item[key] = {"N" if key == "id" else "S": d[key]}

    ddb.put_item(TableName=cli_args_dict['table'], Item=item)
    print('Item with ID ' + d['id'] + ' has been inserted.')


# first line
line = case_file.readline().strip().split(separator)

while line:
    process_line(line)
    line = case_file.readline().strip().split(separator)

case_file.close()
