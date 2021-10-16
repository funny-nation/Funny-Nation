from src.data.casino.table.BlackJackTable import BlackJackTable

from src.data.casino.Casino import Casino
from discord import Client, Message, Member, User


async def blackJackStay(self: Client, message: Message, casino: Casino):
    table: BlackJackTable = casino.getTable(message.channel.id)
    playerID: int = message.author.id
    user: Member = message.author
    if table is None:
        await message.channel.send("这里没人开游戏")
        return
    if not table.hasPlayer(playerID):
        await message.channel.send("你不在这场牌局里")
        return
    table.stay(playerID)
    await message.channel.send(f"玩家{user.display_name}停牌")
    if table.isOver():

        await message.channel.send("牌局结束，正在判断结果")
        winnerID: int = table.endAndGetWinner()
        winner: User = await self.fetch_user(winnerID)

        resultMessage = ''
        for eachPlayerID in table.players:
            eachPlayer = await self.fetch_user(eachPlayerID)
            resultMessage += f"玩家{eachPlayer.display_name}: \n"
            for card in table.viewCards(eachPlayerID):
                resultMessage += card.getString() + '\n'
            resultMessage += '---\n'
        print(resultMessage)
        await message.channel.send(resultMessage)
        await message.channel.send(f"{winner.display_name}胜利")