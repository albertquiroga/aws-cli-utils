import os
import sys
from pscase.utils import TEXT_EDITOR_COMMAND, get_case_path, get_ddb_case_from_case_id


def open_case(args):
    """
    Main function. Queries the DDB table for a case ID and if found, opens its text file.
    :param args: Namespace object containing CLI args
    :return: None
    """
    case = get_ddb_case_from_case_id(args.id)
    _open_case_file(case) if case else _exit_because_no_case_found()


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

