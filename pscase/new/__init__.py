import os
import pyperclip
from pscase.utils.PSCase import PSCase
from pscase.utils import get_case_path, upload_case_to_ddb, TEXT_EDITOR_COMMAND


def _gather_missing_case_info(case):
    """
    Checks the contents of the provided case object, and if there any missing information it will ask the user for it
    :param case: PSCase object representing the case
    :return: Properly-filled args dictionary
    """
    if not case.case_id:
        case.case_id = input("Case ID: ")

    if not case.topic:
        case.topic = input("Case topic: ")

    if not case.title:
        case.title = input("Case title: ")

    if not case.description:
        case.description = input("Description: ")

    if not case.notes:
        case.notes = input("Special notes: ")


def _create_case_file(case_id, test):
    """
    Creates the case text file in the right folder
    :param case_id: Local case ID
    :param test: Boolean flag, if true create in the testing folder instead
    :return: None
    """
    os.system(f'{TEXT_EDITOR_COMMAND} {get_case_path(test)}case{case_id}.txt')


def create_new_case(args):
    case = PSCase.from_namespace(args)
    _gather_missing_case_info(case)
    response = upload_case_to_ddb(case, args.test)
    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code == 200:
        _create_case_file(case.number, args.test)
        pyperclip.copy(case.description)
        print(f"Case {case.number} successfully created.")
    else:
        print(f'Error, HTTP status code was {response_code}')
