import pymysql
import os
import configparser
from loguru import logger


from pymysql import Connection
from pymysql.cursors import Cursor


def makeDatabaseConnection():
    """
    After you use the connection that returned, make sure that you close it.
    db.close()
    :return: pymysql connect instance
    """
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/../../config.ini')
    try:

        db: Connection = pymysql.connect(
            host=config['database']['address'],
            user=config['database']['username'],
            passwd=config['database']['password'],
            database=config['database']['database']
        )
    except Exception as err:
        logger.error(err)
        return None
    return db


def test_makeDatabaseConnection():
    db: Connection = makeDatabaseConnection()
    if db is None:
        raise Exception("Database Connection Error")
    cursor: Cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    db.close()
