import os
import pyperclip
from pscase.utils.PSCase import PSCase
from pscase.utils import get_case_path, upload_case_to_ddb, TEXT_EDITOR_COMMAND


def create_new_case(args):
    """
    Main function. Gathers case data, prompts user for missing info and uploads the case to DDB.
    :param args: Namespace object containing CLI args
    :return: None
    """
    case = _process_cli_args_into_case(args)
    response_code = push_case_to_ddb(case, args.test)

    _successful_ddb_write(case, args.test) if response_code == 200 else _unsuccessful_ddb_write(response_code)


def _process_cli_args_into_case(args):
    """
    Gathers all case data. Turns CLI args inside a namespace object into a PSCase one,
    and then prompts user for missing properties.
    :param args: Namespace object containing CLI args
    :return: PSCase object representing the case
    """
    case = PSCase.from_namespace(args)
    _gather_missing_case_info(case)
    return case


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


def push_case_to_ddb(case, test_flag):
    """
    Uploads a PSCase to the right DDB table and returns the response code
    :param case: PSCase object representing the case
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return:
    """
    response = upload_case_to_ddb(case, test_flag)
    response_code = response['ResponseMetadata']['HTTPStatusCode']
    return response_code


def _unsuccessful_ddb_write(response_code):
    """
    If the response code indicated a failure, inform the user about it
    :param response_code: HTTP response code from DDB
    :return: None
    """
    print(f'Error, HTTP status code was {response_code}')


def _successful_ddb_write(case, test_flag):
    """
    If the response code indicated a success, it creates a new text file for the case,
    copies the description onto the clipboard and informs the user.
    :param case: PSCase object representing the case
    :param test_flag: Boolean flag, if true upload to the testing table instead
    :return: None
    """
    _create_case_file(case.number, test_flag)
    pyperclip.copy(case.description)
    print(f"Case {case.number} successfully created.")


def _create_case_file(case_id, test_flag):
    """
    Creates the case text file in the right folder
    :param case_id: Local case ID
    :param test_flag: Boolean flag, if true create in the testing folder instead
    :return: None
    """
    os.system(f'{TEXT_EDITOR_COMMAND} {get_case_path(test_flag)}case{case_id}.txt')
