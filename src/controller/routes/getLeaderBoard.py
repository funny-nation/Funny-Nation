import sys
import os

from src.model.userManagement import getLeaderBoard
import configparser
from discord import Client, Message, Guild, Member
from pymysql import Connection
from src.utils.readConfig import getLanguageConfig
import embedLib.richList
languageConfig = getLanguageConfig()


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
        for i in range(0, len(leaderBoardData)):
            try:
                userObj: Member or None = await myGuild.fetch_member(leaderBoardData[i][0])
            except Exception as err:
                userObj = None
            if userObj is None:
                userDisplayName = str(languageConfig['leaderBoard']["alternativeNameForNotFound"])
            else:
                userDisplayName: str = userObj.display_name
            moneyDisplay: float = leaderBoardData[i][1] / 100
            embedMsg = embedLib.richList.getEmbed(userDisplayName, moneyDisplay, )
            await message.channel.send(embed=embedMsg)
