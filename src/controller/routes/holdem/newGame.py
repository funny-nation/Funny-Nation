from discord import Client, Message, Member, TextChannel
from pymysql import Connection
from loguru import logger

from src.controller.routes.pauseGame import pauseGame
from src.utils.casino.Casino import Casino
from src.utils.casino.table.holdem.HoldemTable import HoldemTable
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.model.userManagement import addMoneyToUser, getUser
from src.model.cashFlowManagement import addNewCashFlow
from src.model.holdemRecordManagement import newHoldemRecord

from src.model.makeDatabaseConnection import makeDatabaseConnection
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')



async def newHoldemGame(self: Client, message: Message, db: Connection, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    owner: Member = message.author
    channel: TextChannel = message.channel
    userInfo = getUser(db, owner.id)
    if userInfo[1] < 1000:
        await channel.send(f"你的钱有点少，攒攒钱再来")
        return

    if not casino.createHoldemTableByID(owner, channel.id, message):
        await channel.send(f"这个桌子有人用了")
        return

    table: HoldemTable = casino.getTable(channel.id)
    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, owner.id, -table.ante)
    databaseResult = databaseResult and addNewCashFlow(db, owner.id, -table.ante, config['cashFlowMessage']['holdemAnte'])
    databaseResult = databaseResult and newHoldemRecord(db, userInfo[0], table.ante, channel.id, table.uuid)

    if not databaseResult:
        await channel.send(f"炸了，麻烦通知一下群主")
        casino.deleteTable(channel.id)
        return

    casino.onlinePlayer.append(userInfo[0])
    table.addPlayer(userInfo[0])


    await message.add_reaction('\N{White Heavy Check Mark}')
    await channel.send(f"德州扑克牌局已建立，你需要有至少10元，想加入的可以点击上面的✅图标")
    logger.info(f"User {owner.id} created a holdem game")



