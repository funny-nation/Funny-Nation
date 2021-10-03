import pymysql
import configparser
import os


def test_mysqlConnect():
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/../config.ini')
    db = pymysql.connect(host=config['database']['address'], user=config['database']['username'],
                         passwd=config['database']['password'], database=config['database']['database'])
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    db.close()
