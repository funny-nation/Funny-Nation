from src.model.serverInfoManagement import getOnlineMinute, addMinuteOnlineMinute
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection

def test():
    db = makeDatabaseConnection()
    onlineMinute = getOnlineMinute(db)
    assert isinstance(onlineMinute, int)
    assert addMinuteOnlineMinute(db) is True
    assert getOnlineMinute(db) == onlineMinute + 1
    assert addMinuteOnlineMinute(db, -1) is True
    assert getOnlineMinute(db) == onlineMinute
    db.close()
