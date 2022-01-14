from src.model.luckyMoneyManagement import newLuckyMoney, deleteLuckyMoney, takeLuckyMoney, getLuckyMoney, editWhoTake
from src.model.makeDatabaseConnection import makeDatabaseConnection

def test_():
    db = makeDatabaseConnection()
    senderID = 12345
    msgID = 34567
    money = 10000
    quantity = 5
    luckMoneyInfo: tuple = getLuckyMoney(db, msgID)
    if luckMoneyInfo is not None:
        deleteLuckyMoney(db, luckMoneyInfo[0])
    uuid = newLuckyMoney(db, senderID, msgID, quantity, money)
    assert uuid != ''
    assert takeLuckyMoney(db, msgID, 200) is True
    assert editWhoTake(db, msgID, '12345')

    luckMoneyInfo: tuple = getLuckyMoney(db, msgID)
    assert luckMoneyInfo[2] == money - 200
    assert luckMoneyInfo[3] == quantity - 1
    assert luckMoneyInfo[5] == '12345'

    assert deleteLuckyMoney(db, uuid) is True

    db.close()
