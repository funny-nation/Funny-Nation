import re
from discord import User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent, Message
from src.utils.readConfig import getLanguageConfig, getMajorConfig, getGeneralConfig
from pymysql import Connection
from src.model.userManagement import getUser, editUser
from datetime import datetime



async def anonymityBoard(self: Client, message: Message, command: str, db: Connection, anonymityBoardChannel: TextChannel or None):

    languageConfig = getLanguageConfig()
    generalConfig = getGeneralConfig()

    if anonymityBoardChannel is None:
        await message.channel.send(str(languageConfig['anonymityBoard']["noChannelHere"]))
        return

    user: Member = message.author
    userInfo: tuple or None = getUser(db, user.id)
    if userInfo is None:
        await message.channel.send(str(languageConfig['error']["dbError"]))
        return

    now: datetime = datetime.utcnow()
    lastAnonymousMsgTimeStamp: float = datetime.timestamp(userInfo[6])
    nowTimeStamp: float = datetime.timestamp(now)
    coolDownTime: int = int(generalConfig['anonymityBoard']['coolDownTime'])

    if (nowTimeStamp - lastAnonymousMsgTimeStamp) < coolDownTime:
        await message.channel.send(str(languageConfig['anonymityBoard']["tooMuchTalk"]))
        return

    if not editUser(db, user.id, lastAnonymousMsg=now.strftime("%Y-%m-%d %H:%M:%S")):
        await message.channel.send(str(languageConfig['error']["dbError"]))
        return

    anonymousMessage: str = re.findall(f"^匿名 (.+)", command)[0]
    await anonymityBoardChannel.send("```\"" + anonymousMessage + "\"```")

