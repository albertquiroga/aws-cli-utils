# bertolb-tools
Tooling for AWS

## Installation

Start by cloning the repo:

```
git clone https://github.com/albertquiroga/bertolb-tools.git
```

Then install it with pip:

```
pip install --user -e bertolb-tools
```

## Tools
### crawl

```
usage: crawl [-h] location

Crawl an S3 location

positional arguments:
  location    S3 path of the location to be crawled

optional arguments:
  -h, --help  show this help message and exit
```

### ec2

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

## Useful links
### Python modules stuff
* https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
* https://stackoverflow.com/questions/15368054/import-error-on-installed-package-using-setup-py
* https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html
* https://stackoverflow.com/questions/1471994/what-is-setup-py
* https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
* https://stackoverflow.com/questions/27494758/how-do-i-make-a-python-script-executable
