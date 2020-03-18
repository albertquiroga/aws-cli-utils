# AWS CLI Utils
A set of high-level CLI commands to manage and access AWS resources. 

## Installation

Start by cloning the repo:

```
git clone https://github.com/albertquiroga/aws-cli-utils.git
```

Then install it with pip:

```
pip install --user aws-cli-utils
```

## CLI Commands
Right now the package offers commands for EC2, EMR and Glue. 

### EC2
The EC2 command lets you list EC2 instances and then easily connect (SSH) to them by their name tag

```
usage: ec2 [-h] {connect,list} ...

CLI tool to manage EC2 resources

positional arguments:
  {connect,list}

optional arguments:
  -h, --help      show this help message and exit
```

### EMR

The EMR command lets you easily connect (SSH) to EMR clusters by name and list all their information 

```
usage: emr [-h] {connect,info} ...

CLI tool to manage EMR resources

positional arguments:
  {connect,info}

optional arguments:
  -h, --help      show this help message and exit
```

### Glue

The Glue command lets you crawl S3 paths and connect to Development Endpoints and SageMaker notebooks easily by name 

```
usage: glue [-h] {connect,crawl,notebook} ...

CLI tool to manage Glue resources

positional arguments:
  {connect,crawl,notebook}

optional arguments:
  -h, --help            show this help message and exit
```
