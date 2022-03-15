from src.model.activityStatManagement import getActivityStatByUser, addActivityPointToUser, newActivityStatForUser, getAllActivityStat, deleteAllActivityStat
from pymysql import Connection
from src.model.makeDatabaseConnection import makeDatabaseConnection

def test():
    testUserID = 1234
    db = makeDatabaseConnection()
    if getActivityStatByUser(db, testUserID) is not None:
        assert deleteAllActivityStat(db) is True
    assert newActivityStatForUser(db, testUserID) is True
    assert getActivityStatByUser(db, testUserID)[1] == 0
    assert addActivityPointToUser(db, testUserID) is True
    assert getActivityStatByUser(db, testUserID)[1] == 1
    assert getAllActivityStat(db) is not None
    assert deleteAllActivityStat(db) is True
    db.close()
