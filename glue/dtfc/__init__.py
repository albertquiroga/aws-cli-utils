from argparse import Namespace
from typing import Union
import sys

import commons

import boto3
from botocore.exceptions import ClientError

MAX_DELETE_BATCH_SIZE = 100  # Maximum number of tables that can be given to the 'batch_delete_table' operation

glue_client = boto3.client('glue')


def delete_tables_from_crawler(args: Namespace):
    """
    Main function. Gets the output database of the provided crawler, lists all tables within it and deletes
    the ones that were updated by the crawler
    :param args: Namespace object containing CLI args
    :return: None
    """
    database_name = _get_crawler_database(args.name)
    table_names_to_delete = _get_tables_from_crawler(crawler_name=args.name, database_name=database_name)
    _delete_tables(database_name=database_name, table_list=table_names_to_delete)


def _get_crawler_database(crawler_name: str) -> Union[str, None]:
    """
    Gets the output database of a crawler
    :param crawler_name: Name of the target crawler
    :return: If the crawler exists, name of the database. Otherwise, None
    """
    try:
        response = glue_client.get_crawler(Name=crawler_name)
        return response['Crawler']['DatabaseName']
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityNotFoundException':
            print('No crawler was found with that name')
            sys.exit(1)
        else:
            raise ()


def _get_tables_from_crawler(crawler_name: str, database_name: str) -> list:
    """
    Retrieves a list of all tables updated by a particular crawler by getting all tables in the database, then filtering
    those by the 'UPDATED_BY_CRAWLER' property
    :param crawler_name: Name of the target crawler
    :param database_name: Name of the database holding the tables
    :return: List of table names
    """
    table_list = _get_all_tables_in_db(database_name)
    filtered = list(filter(lambda table: table['Parameters']['UPDATED_BY_CRAWLER'] == crawler_name, table_list))
    return list(map(lambda table: table['Name'], filtered))


def _delete_tables(database_name: str, table_list: list):
    """
    Deletes all tables in the provided list
    :param database_name: Name of the database holding the tables
    :param table_list: List of table names to be deleted
    :return: None
    """
    print(f'Deleting {len(table_list)} tables from database {database_name}...')
    split = commons.divide_chunks(table_list, MAX_DELETE_BATCH_SIZE)
    for chunk in split:
        glue_client.batch_delete_table(DatabaseName=database_name, TablesToDelete=chunk)


def _get_all_tables_in_db(database_name: str) -> list:
    """
    Retrieves all tables in a particular database, accounting for pagination
    :param database_name: Name of the target database
    :return: List of tables
    """
    tables = []
    kwargs = {'DatabaseName': database_name}

    while True:
        resp = glue_client.get_tables(**kwargs)
        tables.extend(resp['TableList'])

        try:
            kwargs['NextToken'] = resp['NextToken']
        except KeyError:
            break

    return tables
