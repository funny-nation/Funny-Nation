from src.model.userManagement import addMoneyToUser, editUser, getUser, getLeaderBoard, deleteUser, addNewUser
from pymysql import Connection


def test_():
    from src.model.makeDatabaseConnection import makeDatabaseConnection
    testingTime1 = '2000-01-01 01:01:01'
    testingTime2 = '2001-02-02 02:02:02'
    testingTime3 = '2003-03-03 03:03:03'
    db: Connection = makeDatabaseConnection()
    getUserResult = getUser(db, 123)
    if getUserResult is not None:
        assert deleteUser(db, 123) is True
    assert addNewUser(db, 123) is True
    assert editUser(db, 123, money=1000, lastCheckIn=testingTime1, lastEarnFromMessage=testingTime2, vipLevel=1) is True
    getUserResult = getUser(db, 123)
    assert getUserResult[2].strftime("%Y-%m-%d %H:%M:%S") == testingTime2
    assert getUserResult[3].strftime("%Y-%m-%d %H:%M:%S") == testingTime1
    assert getUserResult[5] == 1
    assert getUserResult[6].strftime("%Y-%m-%d %H:%M:%S") == testingTime3
    assert addMoneyToUser(db, 123, 10)
    getUserResult = getUser(db, 123)
    assert getUserResult[1] == 1010
    assert addMoneyToUser(db, 123, -20)
    assert getUser(db, 123)[1] == 990
    assert getLeaderBoard(db) is not None
    assert deleteUser(db, 123) is True
    assert getUser(db, 123) is None
    db.close()
