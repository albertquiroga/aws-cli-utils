# bertolb-tools
Tooling for AWS

## crawl

```
usage: crawl [-h] location

Crawl an S3 location

positional arguments:
  location    S3 path of the location to be crawled

optional arguments:
  -h, --help  show this help message and exit
```

## ec2

```
usage: ec2 [-h] [-n NAME] [-u USER] [-k KEYPAIR]

Connect and manage EC2 instances

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Connect to the specified EC2 instance name (tag:Name)
  -u USER, --user USER  Username to use in the login
  -k KEYPAIR, --keypair KEYPAIR
                        Path to SSH keypair to use
```
