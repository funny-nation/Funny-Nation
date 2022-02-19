import re

from discord import Client, TextChannel, Message
from pymysql import Connection

import embedLib.anonymousMessage
from src.utils.anonymityBoard.getHashedNameAndColorByUserID import  getHashedChineseNameAndColorByUserID
from src.utils.readConfig import getLanguageConfig


async def anonymityBoard(self: Client, message: Message, command: str, db: Connection, anonymityBoardChannel: TextChannel or None):

    languageConfig = getLanguageConfig()

    if anonymityBoardChannel is None:
        await message.channel.send(str(languageConfig['anonymityBoard']["noChannelHere"]))
        return

    anonymousMessage: str = re.findall(f"^匿名 (.+)", command)[0]
    [anonymousUsername, userColor] = getHashedChineseNameAndColorByUserID(message.author.id)
    embeddedAnonymousMessage = embedLib.anonymousMessage.getEmbed(anonymousMessage, anonymousUsername, __stringToHex(userColor))
    await anonymityBoardChannel.send(embed=embeddedAnonymousMessage)
    await message.channel.send(str(languageConfig['anonymityBoard']['messageSent']))


def __stringToHex(stringToBeConverted: str) -> hex:
    return int(stringToBeConverted, 16)
