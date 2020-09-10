"""
The 'add_rules' modules add scanning rules from a file to the database.
This module supports both Sqlite & Postegres databases.
NOTE: Please make sure that the environment variables are exported.

This command takes one argument:
  path_to_rules     <Required> The path of the file that contains the rules.

Usage:
python -m credentialdigger add_rules /path/rules.yml

"""
import argparse
import logging
import os
import sys

from credentialdigger import PgClient, SqliteClient

logger = logging.getLogger(__name__)


class customParser(argparse.ArgumentParser):
    def error(self, message):
        logger.error(f'{message}')
        self.print_help()
        exit()


parser = customParser()

parser.add_argument(
    'path_to_rules',
    type=str,
    help='<Required> The path of the file that contains the rules.')


def add_rules(*pip_args):
    """
    Add rules to the database

    Parameters
    ----------
    *pip_args
        Keyword arguments for pip.

    Raises
    ------
        FileNotFoundError
            If the file does not exist
        ParserError
            If the file is malformed
        KeyError
            If one of the required attributes in the file (i.e., rules, regex,
            and category) is missing
    """

    args = parser.parse_args(pip_args)

    if os.getenv('USE_PG'):
        logger.info('Use Postgres Client')
        c = PgClient(dbname=os.getenv('POSTGRES_DB'),
                     dbuser=os.getenv('POSTGRES_USER'),
                     dbpassword=os.getenv('POSTGRES_PASSWORD'),
                     dbhost=os.getenv('DBHOST'),
                     dbport=int(os.getenv('DBPORT')))
    else:
        if (os.getenv('SQLITE_DB')):
            logger.info('Use Sqlite Client')
            c = SqliteClient(path=os.getenv('SQLITE_DB'))
        else:
            logger.critical(
                'You did not provide the "SQLITE_DB" environment variable\n'
                '   $ export SQLITE_DB=path_to_database.db')
            sys.exit(-1)

    c.add_rules_from_file(args.path_to_rules)

    # This message will not be logged if the above operation fails, 
    # hence raising an exception.
    logger.info('The rules have been added successfully.')