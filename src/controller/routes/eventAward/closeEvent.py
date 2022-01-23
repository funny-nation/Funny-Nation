import src.model.eventAwardManagement as eventAwardManagement
from discord import Client, TextChannel, Guild, Member, Message
from pymysql import Connection
from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
import list
from src.utils.readConfig import getLanguageConfig, getMajorConfig
import re

async def closeEvent(self: Client, message: Message, db: Connection,eventAdmin: list, command: str):
    author = message.author.id
    eventName: str = re.findall(f"^领奖 .+ [0-9]+$", command)[0]

    if author not in eventAdmin:
        await message.channel.send("失败")
        return

    eventAwardManagement.deletAward(db, message.id)
    await message.channel.send("活动关闭")