import sys
import argparse
from datetime import date

import pscase.utils
import pscase.new
import pscase.open


class PSCase(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Manage AWS PS cases',
            usage='''pscase <command> [<args>]

The most commonly used git commands are:
   new     Create and log a new case
   open    Open a case's file
        '''
        )
        parser.add_argument('command', help='Subcommand to run')

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def new(self):
        parser = argparse.ArgumentParser(
            description='Create and log a new AWS PS case')

        parser.add_argument('--id', action='store', default=str(pscase.utils.last_case_id + 1), help='Local case number')
        parser.add_argument('--date', action='store', type=pscase.utils.date_type, default=date.today().strftime("%m/%d/%y"),
                            help='Date in mm/dd/yy format')
        parser.add_argument('--url', action='store', type=pscase.utils.url_type, help='Case URL')
        parser.add_argument('--title', action='store', help='Case title')
        parser.add_argument('--topic', action='store', help='Case topic')
        parser.add_argument('--description', action='store', help='Description about the issue')
        parser.add_argument('--notes', action='store', help='Any other notes')
        parser.add_argument('--test', action='store_true', help='Write to test DDB table and path instead')
        args = vars(parser.parse_args(sys.argv[2:]))

        pscase.new.main(args)

    def open(self):
        parser = argparse.ArgumentParser(
            description='Open the text file for a case')
        parser.add_argument('id', action='store', help='Paragon case ID')
        args = vars(parser.parse_args(sys.argv[2:]))

        pscase.open.main(args)


if __name__ == '__main__':
    PSCase()


def main():
    PSCase()
