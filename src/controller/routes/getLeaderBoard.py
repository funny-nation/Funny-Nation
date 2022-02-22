import sys
import os

from src.model.userManagement import getLeaderBoard
from discord import Client, Message, Guild, Member
from pymysql import Connection
from src.utils.readConfig import getLanguageConfig
import embedLib.leaderBoard as leaderBoard
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
        try:
            user: Member or None = await myGuild.fetch_member(leaderBoardData[i][0])
        except Exception as err:
            user = None
        if user is None:
            userName = str(languageConfig['leaderBoard']["alternativeNameForNotFound"])
        else:
            userName = user.display_name
        money: float = leaderBoardData[i][1] / 100
        description += f"{i+1}: {userName} - {money}元\n"
        
    embed = leaderBoard.getEmbed(description)
    await message.channel.send(embed=embed)
