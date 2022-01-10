import re
import sys
import os
from loguru import logger
from typing import List, Dict

from src.model.userManagement import getUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow

from discord import Client, Message, Guild, VoiceChannel, VoiceState
from pymysql import Connection

# should be replaced by fetching from database
giftList = {
    '花': 10,
    '火箭': 2000
}


async def liveGift(self: Client, db: Connection, message: Message, command: str):
    userInfo: tuple = getUser(db, message.author.id)
    if userInfo is None:
        await message.channel.send("404")
        logger.error(f"Get user info {message.author.id} failed")
        return

    temp: List[str] = re.findall(f"^礼物 (.+) [1-9][0-9]* \<\@\![0-9]+\>$", command)
    giftName: str = temp[0]
    if giftName not in giftList.keys():
        await message.channel.send('没有这样的礼物')
        return

    myGuild: Guild = self.guilds[0]
    voiceChannels: List[VoiceChannel] = myGuild.voice_channels

    foundIt = False
    for voiceChannel in voiceChannels:
        voiceStates: Dict[int, VoiceChannel] = voiceChannel.voice_states
        if userInfo[0] in voiceStates:
            if message.mentions[0].id not in voiceStates:
                await message.channel.send('该用户并不在同一个频道')
                return
            if not voiceStates[message.mentions[0].id].self_stream:
                await message.channel.send('没有开播哦')
                return
            foundIt = True
    if not foundIt:
        await message.channel.send('没有进语音怎么看直播呢')
        return

    temp: List[str] = re.findall(f"^礼物 .+ ([1-9][0-9]*) \<\@\![0-9]+\>$", command)
    giftNum = int(temp[0])

    money: int = giftNum * giftList.get(giftName) * 100

    if userInfo[1] < money:
        await message.channel.send('没有这么多钱')
        return

    if not addMoneyToUser(db, userInfo[0], -money):
        logger.error(f"Cannot reduce money from user {userInfo[0]}")
        await message.channel.send("404")
        return

    if not addNewCashFlow(db, userInfo[0], -money, '直播礼物'):
        logger.error(f"Cannot create cash flow for user {userInfo[0]}")

    if not addMoneyToUser(db, message.mentions[0].id, money * 0.6):
        logger.error(f"Cannot add money to user {message.mentions[0].id}")
        await message.channel.send("404")
        addNewCashFlow(db, userInfo[0], money, '直播礼物')
        return
    if not addNewCashFlow(db, message.mentions[0].id, money * 0.6, '直播礼物'):
        logger.error(f"Cannot create cash flow for user {message.mentions[0].id}")
        addNewCashFlow(db, userInfo[0], money, '直播礼物')

    await message.channel.send(f"赠送成功 <@{message.mentions[0].id}> 你收到了 {giftName} * {giftNum}")
