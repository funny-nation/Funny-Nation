from loguru import logger
from discord import DMChannel, Client, Message, Member, Guild, User, DMChannel, Client, Member, Guild, Invite, TextChannel, RawReactionActionEvent, Message
import re


async def anonymityBoardTalker(self: Client, message: Message, casino: Casino):


    talker: Member = message.author
    languageConfig = getLanguageConfig()
    userID: int = event.user_id
    messageID: int = event.message_id
    message: str = re.findall(f"^匿名 (.+)", commend, re.S)
    lastAnonymousMsg = now.strftime("%Y-%m-%d %H:%M:%S")
    if now.day != userInfo[3].day: