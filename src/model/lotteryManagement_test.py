from src.model.lotteryManagement import addNewLottery, getLottery, deleteLottery, updateLottery, addNewLotteryRecipient, getLotteryRecipient, deleteLotteryRecipient
from src.model.makeDatabaseConnection import makeDatabaseConnection


def test_():
    db = makeDatabaseConnection()
    publisherId = 12345
    recipientOneId = 54321
    recipientTwoId = 54432
    msgId = 34567
    name = 'random'
    quantity = 5
    price = 10
    isOpen = 0
    if getLottery(db, msgId) is not None:
        deleteLottery(db, msgId)

    assert getLottery(db, msgId) is None
    assert addNewLottery(db, publisherId, msgId, name, price, quantity, isOpen) is True

    lotteryInfo = getLottery(db, msgId)
    print(lotteryInfo)
    assert lotteryInfo is not None
    updateLottery(db, msgId, isOpen=1)
    assert getLottery(db, msgId)[5] is 1
    deleteLottery(db, msgId)

    if getLotteryRecipient(db, msgId) is not None:
        deleteLotteryRecipient(db, msgId)

    assert addNewLotteryRecipient(db, recipientOneId, msgId) is True
    assert addNewLotteryRecipient(db, recipientTwoId, msgId) is True

    recipientInfo = getLotteryRecipient(db, msgId)
    print(recipientInfo)
    assert recipientInfo is not None

    db.close()
