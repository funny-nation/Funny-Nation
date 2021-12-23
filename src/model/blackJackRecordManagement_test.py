from src.model.blackJackRecordManagement import newBlackJackRecord, getBlackJackRecord, getBlackJackRecordsFromATable, dropBlackJackRecord
from src.model.makeDatabaseConnection import makeDatabaseConnection

def test_():
    db = makeDatabaseConnection()
    userID = 123456789
    money = 100
    tableID = 987654321
    tableUUID = "testingUUID"
    blackJackRecord = getBlackJackRecord(db, userID, tableUUID)
    if blackJackRecord is not None:
        assert dropBlackJackRecord(db, userID, tableUUID) is True
    assert newBlackJackRecord(db, userID, money, tableID, tableUUID) is True
    assert getBlackJackRecord(db, userID, tableUUID) is not None
    assert getBlackJackRecordsFromATable(db, tableUUID) is not None
    assert dropBlackJackRecord(db, userID, tableUUID) is True
    db.close()