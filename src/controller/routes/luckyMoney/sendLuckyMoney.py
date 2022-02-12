from discord import Client, Message, User
from pymysql import Connection
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.luckyMoneyManagement import newLuckyMoney
from src.utils.readConfig import getLanguageConfig, getMajorConfig, getCashFlowMsgConfig
import embedLib.luckymoney

async def sendLuckyMoney(self: Client, message: Message, db: Connection, money: int, quantity: int):
    languageConfig = getLanguageConfig()
    cashFlowMsgConfig = getCashFlowMsgConfig()
    memberObject: User = message.author


    if money == 0:
        msg = languageConfig['luckyMoney']['moneyCannotBeZero']\
            .replace('?@user', memberObject.display_name)
        await message.channel.send(msg)
        return


    if quantity == 0:
        msg = languageConfig['luckyMoney']['quantityCannotBeZero']\
            .replace('?@user', memberObject.display_name)
        await message.channel.send(msg)
        return

    if money < quantity:
        msg = languageConfig['luckyMoney']['moneyIsTooLow']\
            .replace('?@user', memberObject.display_name)
        await message.channel.send(msg)
        return

    userInfo: tuple = getUser(db, memberObject.id)

    if userInfo is None:
        msg = languageConfig['luckyMoney']['notEnoughMoney']\
            .replace('?@user', memberObject.display_name)
        await message.channel.send(msg)
        return

    if userInfo[1] < money:
        msg = languageConfig['luckyMoney']['notEnoughMoney'] \
            .replace('?@user', memberObject.display_name)
        await message.channel.send(msg)
        return


    databaseResult = True

    databaseResult = databaseResult and addMoneyToUser(db, memberObject.id, -money)
    databaseResult = databaseResult and addNewCashFlow(db, memberObject.id, -money, cashFlowMsgConfig['luckyMoney']['sendLuckMoney'])

    if not databaseResult:
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return


    embedMsg = embedLib.luckymoney.getEmbed(memberObject.display_name)

    messageSent = await message.channel.send(embed=embedMsg)
    uuid = newLuckyMoney(db, memberObject.id, messageSent.id, quantity, money)
    if uuid == '':
        msg = languageConfig['error']['dbError']
        await message.channel.send(msg)
        return
    await messageSent.add_reaction('💰')


