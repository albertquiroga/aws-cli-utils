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
The EC2 command lets you:

* List all EC2 instances via the 'ec2 list' command

```
usage: ec2 list [-h]

List all EC2 instances

optional arguments:
  -h, --help  show this help message and exit
```

* Connect to a particular instance via SSH by its 'Name' tag using the 'ec2 connect' command

```
usage: ec2 connect [-h] [-k KEY] [-u USER] [-p PORT] [-P] [name]

Connect to an EC2 instance via SSH

positional arguments:
  name                  Name tag of the EC2 instance to connect to

optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Path to private key file to use for authentication
  -u USER, --user USER  Username to be used in the connection
  -p PORT, --port PORT  Port to connect to
  -P, --print           print the SSH command instead of executing it
```

### EMR

The EMR command lets you:

* Connect to an EMR cluster's master node via SSH using the 'emr connect' command

```
usage: emr connect [-h] [-k KEY] [-p] [identifier]

Connect to EMR cluster via SSH

positional arguments:
  identifier         Identifier of the cluster to connect to. This can either
                     be a cluster ID or a "Name" tag

optional arguments:
  -h, --help         show this help message and exit
  -k KEY, --key KEY  Path to private key file to use for auth
  -p, --print        print the SSH command instead of executing it
```

* Print all information about a cluster in a table format using the 'emr info' command

```
usage: emr info [-h] [identifier]

Print information about an EMR cluster

positional arguments:
  identifier  Identifier of the cluster to connect to. This can either be a
              cluster ID or a "Name" tag

optional arguments:
  -h, --help  show this help message and exit
```

### Glue

The Glue command lets you:

* Crawl a particular S3 path using the 'glue crawl' command. The command will either run the first listed crawler that has that path as a target, or create a new one in database 'test' with the path as target 

```
usage: glue crawl [-h] path

Run a crawler

positional arguments:
  path        s3 path to be crawled

optional arguments:
  -h, --help  show this help message and exit
```

* Connect to to a Glue Development Endpoint via SSH using the 'glue connect' command

```
usage: glue connect [-h] [-k KEY] [-p] [name]

Connect to Glue development endpoints

positional arguments:
  name               Name of the dev endpoint to connect to

optional arguments:
  -h, --help         show this help message and exit
  -k KEY, --key KEY  Path to private key file to use for auth
  -p, --print        print the SSH command instead of executing it
```

* Open a Jupyter SageMaker notebook attached to a Glue Development Endpoint in the default browser using the 'glue notebook' command

```
usage: glue notebook [-h] [name]

Connect to a SageMaker Notebook attached to a Dev Endpoint

positional arguments:
  name        Name of the notebook to connect to. Partial match allowed!

optional arguments:
  -h, --help  show this help message and exit
``` 

## Default values

The package supports providing default values for certain parameters of each command. Default values are provided following [the Python-supported .INI file format](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure) and will be read from the '$HOME/.aws-cli-utils' file.

Currently-supported default values are:

### EC2  

The 'ec2 connect' command supports the following values:

* DefaultInstanceName: sets a default value for the 'name' positional argument
* DefaultUsername: sets a default value for the 'username' optional argument
* DefaultPort: sets a default value for the 'port' optional argument

### EMR

Both the 'emr connect' and 'emr info' commands support the following values:

* DefaultClusterIdentifier: sets a default value for the 'identifier' positional argument

### Glue

The 'glue connect' command supports the following values:

* DefaultDevEndpointName: sets a default value for the 'name' positional argument

The 'glue notebook' command supports the following values:

* DefaultNotebookName: sets a default value for the 'name' positional argument

### Sample file

The following is an example of how to write the file:

```
[EC2]
DefaultInstanceName = test
DefaultUsername = ec2-user
DefaultPort = 22

[EMR]
DefaultClusterIdentifier = test

[Glue]
DefaultDevEndpointName = test
DefaultNotebookName = test
```
