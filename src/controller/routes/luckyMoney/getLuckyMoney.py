from discord import Client, TextChannel, Guild, Member
from pymysql import Connection
import src.model.luckyMoneyManagement as luckyMoneyManagement
from src.model.userManagement import addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from typing import List
import json
import random
from src.utils.readConfig import getLanguageConfig, getMajorConfig, getCashFlowMsgConfig



async def getLuckyMoney(self: Client, messageID: int, db: Connection, channelID: int, userID: int):
    languageConfig = getLanguageConfig()
    cashFlowMsgConfig = getCashFlowMsgConfig()


    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(userID)
    channels: List[TextChannel] = myGuild.text_channels
    targetChannel: TextChannel or None = None
    for channel in channels:
        if channel.id == channelID:
            targetChannel = channel
            break


    luckyMoneyInfo = luckyMoneyManagement.getLuckyMoney(db, messageID)
    lastOne = False
    if luckyMoneyInfo[3] == 1:
        lastOne = True

    if luckyMoneyInfo is None:
        msg = languageConfig['luckyMoney']['luckyMoneyDoesNotExist']\
            .replace('?@user', user.display_name)
        await targetChannel.send(msg)
        return

    if luckyMoneyInfo[3] == 0:
        msg = languageConfig['luckyMoney']['luckyMoneyHasAlreadyBeenTaken']\
            .replace('?@user', user.display_name)
        await targetChannel.send(msg)
        return

    whoTake: dict = json.loads(luckyMoneyInfo[5])

    if str(userID) in whoTake:
        msg = languageConfig['luckyMoney']['youHaveAlreadyTaken']\
            .replace('?@user', user.display_name)
        await targetChannel.send(msg)
        return


    if lastOne:
        moneyTakeFromLuckyMoney = luckyMoneyInfo[2]
    else:
        averageMoneyLeft = luckyMoneyInfo[2] / luckyMoneyInfo[3]
        moneyTakeFromLuckyMoney = random.randint(0, int(averageMoneyLeft * 2))

    whoTake[userID] = moneyTakeFromLuckyMoney

    dbResult = True
    dbResult = dbResult and luckyMoneyManagement.takeLuckyMoney(db, messageID, moneyTakeFromLuckyMoney)
    dbResult = dbResult and addMoneyToUser(db, userID, moneyTakeFromLuckyMoney)
    dbResult = dbResult and addNewCashFlow(db, userID, moneyTakeFromLuckyMoney, cashFlowMsgConfig['luckyMoney']['getLuckyMoney'])
    dbResult = dbResult and luckyMoneyManagement.editWhoTake(db, messageID, json.dumps(whoTake))

    if not dbResult:
        msg = languageConfig['error']['dbError']
        await targetChannel.send(msg)
        return
    if moneyTakeFromLuckyMoney == 0:
        msg = languageConfig['luckyMoney']['soSorryThatYouHaveTake0'] \
            .replace('?@user', user.display_name)
        await targetChannel.send(msg)
    else:
        msg = languageConfig['luckyMoney']['congratulationYouHaveTake'] \
            .replace('?@user', user.display_name) \
            .replace('?@money', str(moneyTakeFromLuckyMoney / 100))
        await targetChannel.send(msg)

    if lastOne:
        sender: Member = await myGuild.fetch_member(luckyMoneyInfo[1])
        if sender is None:
            return

        highestTake = 0
        mostLucky = list(whoTake.keys())[0]

        for who in whoTake:
            if highestTake < whoTake[who]:
                mostLucky = who
                highestTake = whoTake[who]

        mostLuckyMember = await myGuild.fetch_member(mostLucky)
        msg = languageConfig['luckyMoney']['noLuckMoneyLeft']\
            .replace('?@sender', sender.display_name)
        await targetChannel.send(msg)
        if mostLuckyMember is None:
            return
        msg = languageConfig['luckyMoney']['theMostLuckyGuy'] \
            .replace('?@user', mostLuckyMember.display_name) \
            .replace('?@money', str(highestTake / 100))
        await targetChannel.send(msg)

