import argparse
from pscase.new import create_new_case
from pscase.open import open_case
from pscase.bulkload import bulk_load
from pscase.utils import last_case_id, date_type
from datetime import date

# Top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# New command
parser_new = subparsers.add_parser('new')
parser_new.add_argument('--number', action='store', default=str(last_case_id + 1), help='Local case number')
parser_new.add_argument('--date', action='store', type=date_type, default=date.today().strftime("%m/%d/%y"),
                        help='Date in mm/dd/yy format')
parser_new.add_argument('--case-id', action='store', help='Paragon case ID')
parser_new.add_argument('--title', action='store', help='Case title')
parser_new.add_argument('--topic', action='store', help='Case topic')
parser_new.add_argument('--description', action='store', help='Description about the issue')
parser_new.add_argument('--notes', action='store', help='Any other notes')
parser_new.add_argument('--test', action='store_true', default=False, help='Write to test DDB table and path instead')
parser_new.set_defaults(func=create_new_case)

# Open command
parser_open = subparsers.add_parser('open')
parser_open.add_argument('id', action='store', help='Paragon case ID')
parser_open.set_defaults(func=open_case)

# Bulkload command
parser_bulkload = subparsers.add_parser('bulkload')
parser_bulkload.add_argument('file', help='TSV file to upload')
parser_bulkload.add_argument('--test', action='store_true', default=False, help='Load to test DDB table instead')
parser_bulkload.set_defaults(func=bulk_load)


def main():
    args = parser.parse_args()

    if not len(vars(args)) == 0:
        args.func(args)
    else:
        parser.print_help()
