
from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.model.holdemRecordManagement import newHoldemRecord, removeHoldemRecord, getHoldemRecord, setHoldemRecordStatus


def test_():
    db = makeDatabaseConnection()
    assert db is not None
    tableUUID = "abcdefg"
    holdemRecord = getHoldemRecord(db, 123, tableUUID)
    if holdemRecord is not None:
        assert removeHoldemRecord(db, 123, tableUUID) is True
    assert newHoldemRecord(db, 123, 100, 123123, tableUUID) is True
    assert setHoldemRecordStatus(db, 123, tableUUID, 1) is True
    holdemRecord = getHoldemRecord(db, 123, tableUUID)
    assert holdemRecord is not None
    assert holdemRecord[2] == 1
    assert removeHoldemRecord(db, 123, tableUUID) is True
    assert getHoldemRecord(db, 123, tableUUID) is None
    db.close()
