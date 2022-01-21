from src.model.eventAwardManagement import newAward, deletAward, takeAward, editRecipient, getEventAward
from src.model.makeDatabaseConnection import makeDatabaseConnection

def test_():
    db = makeDatabaseConnection()
    eventManagerID = 123456
    eventMsgID = 123456
    money = 100
    eventName = "testing"
    recipient = "1561516161"
    eventAwardInfo: tuple = getEventAward(db, eventMsgID)
    if eventAwardInfo is not None:
        deletAward(db, eventAwardInfo[0])
    uuid = newAward(db, eventManagerID, eventMsgID, money, eventName)
    assert uuid != ""
    assert takeAward(db, eventManagerID, 200) is True
    assert editRecipient(db, eventMsgID, recipient)

    eventAwardInfo: tuple = getEventAward(db, eventMsgID)
    assert eventAwardInfo[5] == recipient

    assert deletAward(db, uuid) is True

    db.close()






