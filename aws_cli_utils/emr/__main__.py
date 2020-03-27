import sys

from aws_cli_utils.emr.EMRCLI import EMRCLI


def main():
    EMRCLI().main()


if __name__ == '__main__':
    sys.exit(main())
