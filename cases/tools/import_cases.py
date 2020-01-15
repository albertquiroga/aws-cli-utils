import boto3

case_file = open('/Users/bertolb/cases.txt', 'r')
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

    ddb.put_item(TableName='cases', Item=item)
    print('Item with ID ' + d['id'] + ' has been inserted.')


# first line
line = case_file.readline().strip().split(separator)

while line:
    process_line(line)
    line = case_file.readline().strip().split(separator)

case_file.close()
