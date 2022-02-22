
from discord import Client, TextChannel, Member, Guild

from pymysql import Connection

from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.runWhenBotStart.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.utils.poker.pokerImage import getPokerImage
from src.model.userManagement import addMoneyToUser
from src.model.holdemRecordManagement import setHoldemRecordStatus
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getCashFlowMsgConfig
cashFlowMsgConfig = getCashFlowMsgConfig()


async def holdemEndGame(table: HoldemTable, channel: TextChannel, self: Client, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting, publicForCards = True):
    await channel.send("游戏结束，正在判断赢家")
    table.generateSidePots()
    result = table.end()
    endingMSG = ""
    databaseResult = True
    myGuild: Guild = self.guilds[0]
    for winner in result:
        databaseResult = databaseResult and setHoldemRecordStatus(db, winner, table.uuid, 2)
        databaseResult = databaseResult and addMoneyToUser(db, winner, result[winner])
        databaseResult = databaseResult and addNewCashFlow(db, winner, result[winner], cashFlowMsgConfig['holdem']['holdemWin'])
        member: Member = await myGuild.fetch_member(winner)
        moneyDisplay = result[winner] / 100
        endingMSG += f"玩家{member.display_name}获得{moneyDisplay}元\n"


    for eachPlayerID in table.players:
        casino.onlinePlayer.remove(eachPlayerID)
        if eachPlayerID not in result:
            databaseResult = databaseResult and setHoldemRecordStatus(db, eachPlayerID, table.uuid, 1)

    if publicForCards:
        for eachPlayerID in table.players:
            if not table.players[eachPlayerID]['fold']:
                eachPlayer = await myGuild.fetch_member(eachPlayerID)
                await channel.send(f"玩家{eachPlayer.display_name}的牌: ")
                cards = table.viewCards(eachPlayerID)
                await channel.send(file=getPokerImage(cards))

    await channel.send(endingMSG)
    casino.deleteTable(channel.id)
    return
