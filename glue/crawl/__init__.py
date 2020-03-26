from argparse import Namespace
from functools import reduce
from typing import Union

from common_utils.aws import glue_client


def crawl(args: Namespace):
    """
    Main function. Looks for existing crawlers already targeting the provided path. If there's one, it will run it.
    Otherwise, it will create one for it and run it.
    :param args: Namespace object containing CLI args
    :return: None
    """
    crawler_name = _look_for_existing_crawler(args.path)
    _run_existing_crawler(crawler_name) if crawler_name else _create_and_run_crawler(args.path, args.database)


def _look_for_existing_crawler(s3_location: str):
    """
    Checks whether a crawler already exists with the specified S3 path as the target, and if
    there is it returns its name. If there's several, return the first
    :param s3_location: S3 path to be crawled
    :return: Name of the crawler, or None
    """
    crawler_list = glue_client.get_crawlers()['Crawlers']
    return _process_crawlers(crawler_list, s3_location) if crawler_list else None


def _process_crawlers(crawler_list: list, s3_location: str) -> Union[str, None]:
    """
    Given a list of crawlers, it will check their targets to see if they contain the provided s3 location.
    If they do, it will return the first one.
    :param crawler_list: List of crawlers
    :param s3_location: S3 path to be crawled
    :return: Name of the first encountered crawler that has the path on its targets
    """
    def _filter_crawler(crawler: dict) -> bool:
        """
        Returns true if s3_location is in the crawler's targets
        :param crawler: Crawler to be filtered
        :return: True if s3_location is in the crawler's targets, False otherwise
        """
        targets = list(map(lambda s3_target: s3_target['Path'], crawler['Targets']['S3Targets']))
        return s3_location in targets

    filtered_crawlers = list(filter(_filter_crawler, crawler_list))
    crawler_names = list(map(lambda crawler: crawler['Name'], filtered_crawlers))
    return reduce(lambda a, b: a, crawler_names) if len(crawler_names) > 0 else None


def _run_existing_crawler(crawler_name: str):
    """
    Runs the specified crawler
    :param crawler_name: Name of the crawler to run
    :return: None
    """
    print(f'Crawler found for the specified location. Running crawler {crawler_name}')
    glue_client.start_crawler(Name=crawler_name)


def _create_and_run_crawler(s3_location: str, database_name: str):
    """
    Creates a new crawler targeting the specified S3 path, then runs it.
    :param s3_location: S3 path to crawl
    :return: None
    """
    crawler_name = s3_location.split('/')[-2]
    print(f'Creating new crawler: {crawler_name}')
    glue_client.create_crawler(
        Name=crawler_name,
        Role='service-role/AWSGlueServiceRole-DefaultRole',
        DatabaseName=database_name,
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

    print(f'Running new crawler: {crawler_name}')
    glue_client.start_crawler(Name=crawler_name)
