import sys
import os

from src.model.userManagement import getLeaderBoard
import configparser
from discord import Client, Message, Guild, Member
from pymysql import Connection
languageConfig = configparser.ConfigParser()
languageConfig.read('Language.ini', encoding='utf-8')

config = configparser.ConfigParser()
config.read("Cconfig.ini")

async def getLeaderBoardTop10(self: Client, message: Message, db: Connection):
    """
    Reply for leader board top 10
    :param self: Client obj
    :param message: Message Obj
    :param db: Database obj
    :return: None
    """
    leaderBoardData: tuple = getLeaderBoard(db)
    myGuild: Guild = self.guilds[0]
    if leaderBoardData is None:
        systemError = str(languageConfig['error']["dbError"])
        messageSendBack: str = systemError
    else:
        messageSendBack = "以下为本DC最有钱的大佬：\n"
        for i in range(0, len(leaderBoardData)):
            try:
                userObj: Member or None = await myGuild.fetch_member(leaderBoardData[i][0])
            except Exception as err:
                userObj = None
            if userObj is None:
                systemError = str(languageConfig['latter']["error"])
                userDisplayName = systemError
            else:
                userDisplayName: str = userObj.display_name
            moneyDisplay: float = leaderBoardData[i][1] / 100
            messageSendBack += f"{i + 1}： {userDisplayName} - {moneyDisplay}元\n"

    await message.channel.send(messageSendBack)