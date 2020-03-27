import sys

from aws_cli_utils.glue.GlueCLI import GlueCLI


def main():
    GlueCLI().main()


if __name__ == '__main__':
    sys.exit(main())
