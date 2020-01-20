import re
import sys
from urllib.parse import urlparse


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
    new_prompt = f'{prompt} [{default}]: ' if default else f'{prompt}: '
    data = read_input(new_prompt)

    if data and regex:
        return match_against_regex(data, regex)
    else:
        return data if data else default


def gather_case_info(args):
    if not args['topic']:
        args['topic'] = ask_for_input("Case topic")

    if not args['title']:
        args['title'] = ask_for_input("Case title")

    if not args['url']:
        args['url'] = ask_for_input("Case URL")

    if not args['description']:
        args['description'] = ask_for_input("Description")

    if not args['notes']:
        args['notes'] = ask_for_input("Special notes")

    args['case_id'] = urlparse(args['url']).query.split('=')[1]

    return args
