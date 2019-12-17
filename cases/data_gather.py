import re
import sys
from datetime import date

DATE_REGEX = '^\d{2}\/\d{2}\/\d{2}$'
LINK_REGEX = 'https:\/\/paragon-na\.amazon\.com\/hz\/view-case\?caseId=\d+'


def read_input(prompt):
    if sys.version_info > (3, 0):
        # Python 3 code in this block
        return input(prompt)
    else:
        # Python 2 code in this block
        return raw_input(prompt)


def match_against_regex(data, regex):
    if re.match(regex, data):
        return data
    else:
        print("Input didn't match expected regex format: " + regex)
        exit(1)


def ask_for_input(prompt, default=None, regex=None):
    new_prompt = (prompt + ' [%s]: ' % default) if default else (prompt + ': ')
    data = read_input(new_prompt)
    if data and regex:
        return match_against_regex(data, regex)
    else:
        return data if data else default


def gather_case_info(case_number):
    case_info = {
        'id': ask_for_input("ID", default=str(case_number)),
        'date': ask_for_input("Date", default=date.today().strftime("%m/%d/%y"), regex=DATE_REGEX),
        'topic': ask_for_input("Case topic"),
        'name': ask_for_input("Case title"),
        'link': ask_for_input("Case url", regex=LINK_REGEX),
        'description': (ask_for_input("Case description") or ""),
        'special stuff': (ask_for_input("Case special notes") or "")
    }

    case_info['caseid'] = case_info['link'].split('=')[1]  # TODO change this to properly get the URL's queryparam

    return case_info
