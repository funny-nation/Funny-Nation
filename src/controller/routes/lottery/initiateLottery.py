import re

from discord import Client, User, Message
from pymysql import Connection

import embedLib.lotteryAnnouncement
from src.model.lotteryManagement import addNewLottery
from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()


async def initiateLottery(self: Client, message: Message, db: Connection, command: str):
    result: tuple = re.findall(f"^抽奖 (.+) ([\\-0-9]+) ([\\-0-9]+)$", command)[0]
    name: str = result[0]
    price: int = int(result[1])
    quantity: int = int(result[2])
    publisher: User = message.author

    # Lottery price check
    if price < 0 or type(price) != int:
        await publisher.send(languageConfig['lottery']['priceError'])
        return

    # Lottery quantity check
    if quantity < 1 or type(quantity) != int:
        await publisher.send(languageConfig['lottery']['quantityError'])
        return

    embed_msg = embedLib.lotteryAnnouncement.getEmbed(publisher, name, price, quantity)
    sent_message: Message = await message.channel.send(embed=embed_msg)

    systemError: str = str(languageConfig['error']["dbError"])
    response: bool = addNewLottery(db, publisher.id, sent_message.id, name, price * 100, quantity, 0)

    if response is False:
        await message.channel.send(systemError)
        return

    await sent_message.add_reaction('🎟️')
    await sent_message.add_reaction('🟩')
    await sent_message.add_reaction('🟥')
