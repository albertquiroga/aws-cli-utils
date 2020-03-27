import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
emr_client = boto3.client('emr')
glue_client = boto3.client('glue')
sagemaker_client = boto3.client('sagemaker')
