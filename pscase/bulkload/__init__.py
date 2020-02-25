import csv
from pscase.utils.PSCase import PSCase
from pscase.utils import upload_case_to_ddb


def _import_tsv_file(file_path, test_flag):
    with open(file_path, newline='') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for line in reader:
            case = PSCase.from_dictionary(line)
            response = upload_case_to_ddb(case, test_flag)
            response_code = response['ResponseMetadata']['HTTPStatusCode']
            if response_code == 200:
                print(f'Successfully uploaded case {case.number}')


def bulk_load(args):
    _import_tsv_file(args.file, args.test)
