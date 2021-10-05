import sys
import os

sys.path.append(os.path.dirname(__file__) + '/../../model')
import userManagement


async def checkBalance(message, db):
    user = message.author
    userInfo = userManagement.getUser(db, user.id)
    messageSendBack = ''
    if userInfo is None:
        messageSendBack = '系统错误'
    else:
        displayMoney = userInfo[1] / 100
        messageSendBack = f"{user.display_name}，你还有{displayMoney}元"
    await message.channel.send(messageSendBack)
