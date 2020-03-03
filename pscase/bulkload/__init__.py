import csv
from pscase.utils.PSCase import PSCase
from pscase.utils import upload_case_to_ddb


def bulk_load(args):
    """
    Main function.
    :param args: Namespace object containing CLI args
    :return: None
    """
    _import_tsv_file(args.file, args.test)


def _import_tsv_file(file_path, test_flag):
    """
    Opens a TSV file and processes each line as a case.
    :param file_path: Path to the TSV file
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return: None
    """
    with open(file_path, newline='') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for line in reader:
            _process_line(line, test_flag)


def _process_line(line, test_flag):
    """
    Process each line in the data file. Turn each line into a case, upload it to DDB and check the response code.
    :param line: Line to be processed
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return: None
    """
    case = PSCase.from_dictionary(line)
    response = upload_case_to_ddb(case, test_flag)
    response_code = response['ResponseMetadata']['HTTPStatusCode']
    if response_code == 200:
        print(f'Successfully uploaded case {case.number}')
