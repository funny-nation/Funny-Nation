import re
from discord import User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent, Message
from src.utils.readConfig import getLanguageConfig, getMajorConfig
from pymysql import Connection
from src.model.userManagement import getUser
from datetime import datetime



async def anonymityBoardTalker(self: Client, message: Message, event: RawReactionActionEvent, command: str, db: Connection, anonymityBoardChannel):


    user: Member = message.author
    languageConfig = getLanguageConfig()
    now: datetime = datetime.utcnow()
    userID: int = event.user_id
    messageID: int = event.message_id
    message: str = re.findall(f"^匿名 (.+)", command, re.S)
    userInfo: tuple = getUser(db, userID)
    lastAnonymousMsg = now.strftime("%Y-%m-%d %H:%M:%S")
    if now.day != userInfo[3].day:
        await anonymityBoardChannel.send(message)
        return
    else:
        await message.channel.send(str(languageConfig['anonymityBoard']["tooMuchTalk"]))
        return

