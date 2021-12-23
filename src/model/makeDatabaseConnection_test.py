
from pymysql import Connection
from pymysql.cursors import Cursor
from src.model.makeDatabaseConnection import makeDatabaseConnection


def test_():
    db: Connection = makeDatabaseConnection()
    if db is None:
        raise Exception("Database Connection Error")
    cursor: Cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    db.close()
