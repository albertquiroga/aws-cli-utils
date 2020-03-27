import sys

from aws_cli_utils.ec2.EC2CLI import EC2CLI


def main():
    EC2CLI().main()


if __name__ == '__main__':
    sys.exit(main())
