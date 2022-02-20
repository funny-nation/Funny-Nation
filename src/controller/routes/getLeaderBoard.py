import sys
import os

from src.model.userManagement import getLeaderBoard
import configparser
from discord import Client, Message, Guild, Member
from pymysql import Connection
from src.utils.readConfig import getLanguageConfig
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
    description: str = ""
    if leaderBoardData is None:
        systemError = str(languageConfig['error']["dbError"])
        await message.channel.send(systemError)
        return

    for i in range(0, len(leaderBoardData)):
        userName: Member = myGuild.get_member(leaderBoardData[i][0])
        money: float = leaderBoardData[i][1] / 100
        description += f"{i+1}: {userName} - {money}元\n"
        


        await message.channel.send(description)
