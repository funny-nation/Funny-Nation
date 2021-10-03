import pymysql
import os
import configparser
from loguru import logger


def makeDatabaseConnection():
    """
    After you use the connection that returned, make sure that you close it.
    db.close()
    :return: pymysql connect instance
    """
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/../../config.ini')
    try:

        db = pymysql.connect(
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
    db = makeDatabaseConnection()
    if db is None:
        raise Exception("Database Connection Error")
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    db.close()
