from discord import Client, TextChannel, Guild, Member, Message, Embed
from pymysql import Connection
import src.model.luckyMoneyManagement as luckyMoneyManagement
from src.model.userManagement import addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from typing import List
import json
import random
from src.utils.readConfig import getLanguageConfig, getMajorConfig, getCashFlowMsgConfig
import embedLib.luckymoney as luckyMoneyEmbed



async def getLuckyMoney(self: Client, messageID: int, db: Connection, channelID: int, userID: int):
    languageConfig = getLanguageConfig()
    cashFlowMsgConfig = getCashFlowMsgConfig()


    myGuild: Guild = self.guilds[0]
    user: Member = await myGuild.fetch_member(userID)
    targetChannel: TextChannel = myGuild.get_channel(channelID)
    message: Message = await targetChannel.fetch_message(messageID)
    messageEmbed: Embed = message.embeds[0]


    luckyMoneyInfo = luckyMoneyManagement.getLuckyMoney(db, messageID)
    lastOne = False
    if luckyMoneyInfo[3] == 1:
        lastOne = True

    if luckyMoneyInfo is None: # lucky money does not existed
        return

    if luckyMoneyInfo[3] == 0: # lucky money has already been taken
        return

    whoTake: dict = json.loads(luckyMoneyInfo[5])

    if str(userID) in whoTake:
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
        luckyMoneyEmbed.newPersonWithZero(messageEmbed, user.display_name)
        await message.edit(embed=messageEmbed)

    else:
        luckyMoneyEmbed.newPerson(messageEmbed, user.display_name, str(moneyTakeFromLuckyMoney / 100))
        await message.edit(embed=messageEmbed)

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
        if mostLuckyMember is None:
            return
        luckyMoneyEmbed.addBestLuck(messageEmbed, mostLuckyMember.display_name, str(highestTake / 100))
        await message.edit(embed=messageEmbed)

