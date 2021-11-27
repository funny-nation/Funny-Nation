import pymysql
import os
import configparser
from loguru import logger


from pymysql import Connection
from pymysql.cursors import Cursor

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")


def makeDatabaseConnection():
    """
    After you use the connection that returned, make sure that you close it.
    db.close()
    :return: pymysql connect instance
    """
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
