import json

from src.model.eventAwardManagement import newAward, removeRecipient, getEventAward, addRecipient,deletAward, searchRecipientsByPrivateMSGID, approveRecipients, rejectRecipients, closeEvent, getEventAwardByName, searchRecipientByEventIDandRecipientID
from src.model.makeDatabaseConnection import makeDatabaseConnection
from typing import List

def test_():
    db = makeDatabaseConnection()
    assert db is not None
    eventManagerID = 123456
    eventMsgID = 123456
    money = 300
    eventName = '+testing+'
    recipientMSGID = 123456
    recipientID = 123456
    eventAwardInfo: tuple = getEventAward(db, eventMsgID)
    if eventAwardInfo is not None:
        deletAward(db, eventAwardInfo[1])
    assert newAward(db, eventManagerID, eventMsgID, money, eventName) is True
    assert getEventAwardByName(db, eventName) is not None
    assert addRecipient(db, eventMsgID, recipientMSGID, recipientID) is True
    assert searchRecipientsByPrivateMSGID(db, recipientMSGID) is not None
    assert approveRecipients(db, recipientMSGID) is True
    assert rejectRecipients(db, recipientMSGID) is True
    assert searchRecipientByEventIDandRecipientID(db, eventMsgID, recipientID) is not None
    assert removeRecipient(db, eventMsgID) is True
    assert closeEvent(db, eventMsgID) is True
    assert getEventAwardByName(db, eventName) is None
    assert deletAward(db, eventMsgID) is True

    db.close()






