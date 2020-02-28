import os
import sys
from pscase.utils import TEXT_EDITOR_COMMAND, get_case_path, get_ddb_case_from_case_id, get_ddb_case_from_number

_PARAGON_URL_BASE = 'https://paragon-na.amazon.com/hz/view-case?caseId='


def open_case(args):
    """
    Main function. Queries the DDB table for a case ID and if found, opens its text file.
    :param args: Namespace object containing CLI args
    :return: None
    """
    _open_case_from_case_id(args.case_id) if args.id is not None else _open_case_from_case_number(args.number)


def _open_case_from_case_id(case_id):
    """
    Uses the case_id provided via CLI to find its case and open its local case file
    :param case_id: Paragon case ID of the case to be opened
    :return: None
    """
    case = get_ddb_case_from_case_id(case_id)
    _open_case_file(case) if case else _exit_because_no_case_found()


def _open_case_from_case_number(number):
    """
    Uses the number provided via CLI to find its case and open it in Paragon
    :param number: Case number of the case to be opened
    :return: None
    """
    case = get_ddb_case_from_number(number)
    _open_paragon_case(case) if case else _exit_because_no_case_found()


def _open_paragon_case(case):
    """
    Opens a Paragon case on the browser by using its case ID
    :param case: PSCase object with the case data
    :return: None
    """
    os.system(f'open {_PARAGON_URL_BASE}{case.case_id}')


def _open_case_file(case):
    """
    Opens a given case's text file
    :param case: Dictionary containing the case data
    :return: None
    """
    print(f'Opening case {case.case_id}')
    os.system(f'{TEXT_EDITOR_COMMAND} {get_case_path()}case{case.number}.txt')


def _exit_because_no_case_found():
    """
    Print an error message and exit if no matching case was found in the DDB table
    :return: None
    """
    print('Case not found in DDB table')
    sys.exit(1)

