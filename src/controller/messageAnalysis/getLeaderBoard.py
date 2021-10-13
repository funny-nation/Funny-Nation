import sys
import os

from src.model.userManagement import getLeaderBoard


async def getLeaderBoard(self, message, db):
    """
    Reply for leader board top 10
    :param self: Client obj
    :param message: Message Obj
    :param db: Database obj
    :return: None
    """
    leaderBoardData = getLeaderBoard(db)
    myGuild = self.guilds[0]
    messageSendBack = ''
    if leaderBoardData is None:
        messageSendBack = '系统错误'
    else:
        messageSendBack = "以下为本DC最有钱的大佬：\n"
        for i in range(0, len(leaderBoardData)):
            userObj = await myGuild.fetch_member(leaderBoardData[i][0])
            userDisplayName = ""
            if userObj is None:
                userDisplayName = "不知道是谁"
            else:
                userDisplayName = userObj.display_name
            moneyDisplay = leaderBoardData[i][1] / 100
            messageSendBack += f"{i + 1}： {userDisplayName} - {moneyDisplay}元\n"

    await message.channel.send(messageSendBack)