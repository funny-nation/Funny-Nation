from src.model.userManagement import getUser

from discord import Client, Message, User, DMChannel
from pymysql import Connection
from src.data.casino.Casino import Casino
from src.data.casino.table import Table, BlackJackTable


async def joinGame(self: Client, message: Message, db: Connection, casino: Casino):
    table: Table = casino.getTable(message.channel.id)
    playerID = message.author.id
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if table.hasPlayer(playerID):
        await message.channel.send("你已经加入了")
        return
    userInfo: tuple = getUser(db, playerID)
    if userInfo[1] < table.money:
        await message.channel.send("你好像不太够钱")
        return

    if table.game == 'blackJack':
        table: BlackJackTable
        table.addPlayer(playerID)
        if not table.gameStart():
            await message.channel.send("炸了")
            return

        await message.channel.send("开始了，底牌已经私聊你们了，请各位查看自己的牌")

        for userID in table.players:
            user: User = await self.fetch_user(userID)
            dmChannel: DMChannel = await user.create_dm()
            await dmChannel.send("这是你的牌：")
            cards = table.viewCards(userID)
            for card in cards:
                await dmChannel.send(card.getString())
            await dmChannel.send("你还要牌吗")

