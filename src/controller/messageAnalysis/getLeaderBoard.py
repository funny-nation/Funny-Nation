import sys
import os

sys.path.append(os.path.dirname(__file__) + '/../../model')
import userManagement


async def getLeaderBoard(self, message, db):
    leaderBoardData = userManagement.getLeaderBoard(db)
    myGuild = self.guilds[0]
    print(message.author.id)
    messageSendBack = ''
    if leaderBoardData is None:
        messageSendBack = '系统错误'
    else:
        messageSendBack = "以下为本DC最有钱的大佬：\n"
        for i in range(0, len(leaderBoardData) - 1):
            userObj = await myGuild.fetch_member(leaderBoardData[i][0])
            userDisplayName = ""
            if userObj is None:
                userDisplayName = "不知道是谁"
            else:
                userDisplayName = userObj.display_name
            moneyDisplay = leaderBoardData[i][1] / 100
            messageSendBack += f"{i + 1}： {userDisplayName} - {moneyDisplay}元\n"

    await message.channel.send(messageSendBack)