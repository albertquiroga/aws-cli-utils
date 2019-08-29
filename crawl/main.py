import boto3
import argparse
from bertolb_utils import format_location

glue = boto3.client('glue')

parser = argparse.ArgumentParser(prog='crawl', description='Crawl an S3 location')
parser.add_argument('location', help='S3 path of the location to be crawled')

cli_args_dict = vars(parser.parse_args())

s3_path = format_location(cli_args_dict['location'])
print('Target location: ' + s3_path)


def look_for_existing_crawler(s3_location):
    """
    Checks whether a crawler already exists with the specified S3 path as the target, and if
    there is it returns its name
    :param s3_location: S3 path to be crawled
    :return: Name of the crawler
    """
    crawlers_list = glue.get_crawlers()
    for crawler in crawlers_list['Crawlers']:
        s3_paths = map(lambda x: x['Path'], crawler['Targets']['S3Targets'])

        if s3_location in s3_paths:
            return crawler['Name']


def run_crawler(crawler_name):
    """
    Runs the specified crawler
    :param crawler_name: Name of the crawler to run
    :return: None
    """
    print('Crawler found for the specified location. Running crawler ' + crawler_name)
    glue.start_crawler(Name=crawler_name)


def create_and_run_crawler(s3_location):
    """
    Creates a new crawler targeting the specified S3 path, then runs it.
    :param s3_location: S3 path to crawl
    :return: None
    """
    crawler_name = s3_location.split('/')[-2]
    print('Creating new crawler: ' + crawler_name)
    glue.create_crawler(
        Name=crawler_name,
        Role='service-role/AWSGlueServiceRole-DefaultRole',
        DatabaseName='test',
        Targets={
            'S3Targets': [
                {
                    'Path': s3_location,
                    'Exclusions': []
                }
            ],
            'JdbcTargets': [],
            'DynamoDBTargets': [],
            'CatalogTargets': []
        }
    )

    print('Running new crawler: ' + crawler_name)
    glue.start_crawler(Name=crawler_name)


def crawl():
    """
    Main function. Looks for a crawler already crawling the provided S3 path. If it does exist, it will
    run the crawler. If it doesn't, it will create a new one and run it.
    :return: None
    """
    existing_crawler_name = look_for_existing_crawler(s3_path)
    run_crawler(existing_crawler_name) if existing_crawler_name else create_and_run_crawler(s3_path)
