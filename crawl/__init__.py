import boto3
import argparse
import sys
import myutils

glue = boto3.client('glue')

parser = argparse.ArgumentParser(prog='crawl', description='Crawl an S3 location')
parser.add_argument('location', help='S3 path of the location to be crawled')

cli_args_dict = vars(parser.parse_args())


def run():
    location = myutils.format_location(cli_args_dict['location'])
    print('Target location: ' + location)

    # First we check if there's any crawler that's already crawling that location
    crawlers_list = glue.get_crawlers()
    for crawler in crawlers_list['Crawlers']:
        s3_paths_list = crawler['Targets']['S3Targets']
        run_flag = False

        for path in s3_paths_list:
            if path['Path'] == location:
                print('Crawler found for the specified location')
                run_flag = True

        if run_flag:
            print('Running crawler ' + crawler['Name'])
            print(glue.start_crawler(Name=crawler['Name']))
            sys.exit()

    # If not, create a new crawler and run it
    crawler_name = location.split('/')[-2]

    print('Creating new crawler: ' + crawler_name)
    glue.create_crawler(
        Name=crawler_name,
        Role='service-role/AWSGlueServiceRole-DefaultRole',
        DatabaseName='test',
        Targets={
            'S3Targets': [
                {
                    'Path': location,
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
