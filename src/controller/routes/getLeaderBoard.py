import sys
import os

from src.model.userManagement import getLeaderBoard
import configparser
from discord import Client, Message, Guild, Member, Embed
from pymysql import Connection
from src.utils.readConfig import getLanguageConfig
import embedLib.leaderBoard as leaderBoardEmbed
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
        await message.channel.send(languageConfig['error']["dbError"])
        return

    description: str = ""

    for i in range(0, len(leaderBoardData)):
        userID: int = leaderBoardData[i][0]
        money: int = leaderBoardData[i][1]
        try:
            member: Member = await myGuild.fetch_member(userID)
            displayName = member.display_name
        except Exception:
            displayName = languageConfig['leaderBoard']['alternativeNameForNotFound']
        description += f"{i + 1}: {displayName} - {money / 100}\n"

    embed: Embed = leaderBoardEmbed.getEmbed(description)
    await message.channel.send(embed=embed)



