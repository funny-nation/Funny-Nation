import sys
import os

from src.model.userManagement import getLeaderBoard

from discord import Client, Message, Guild, Member
from pymysql import Connection


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
        messageSendBack = '系统错误'
    else:
        messageSendBack = "以下为本DC最有钱的大佬：\n"
        for i in range(0, len(leaderBoardData)):
            userObj: Member = await myGuild.fetch_member(leaderBoardData[i][0])
            userDisplayName = ""
            if userObj is None:
                userDisplayName = "不知道是谁"
            else:
                userDisplayName: str = userObj.display_name
            moneyDisplay: float = leaderBoardData[i][1] / 100
            messageSendBack += f"{i + 1}： {userDisplayName} - {moneyDisplay}元\n"

    await message.channel.send(messageSendBack)