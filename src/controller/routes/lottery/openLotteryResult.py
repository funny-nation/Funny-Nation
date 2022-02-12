import random

from discord import Client, Message, Member, PartialEmoji, User
from pymysql import Connection

import embedLib.lotteryResult
from src.model.lotteryManagement import getLottery, updateLottery, getLotteryRecipient
from src.utils.readConfig import getLanguageConfig

languageConfig = getLanguageConfig()


async def openLotteryResult(self: Client, db: Connection, userId: int, msgId: int, member: Member, channelId: int, emoji: PartialEmoji):
    recipientIdList: list = list(map(lambda x: x[0], getLotteryRecipient(db, msgId)))
    lotteryInfo: tuple = getLottery(db, msgId)
    reward = lotteryInfo[2]
    quantity = lotteryInfo[3]
    isOpen = lotteryInfo[5]

    channel = self.get_channel(channelId)
    message: Message = await channel.fetch_message(msgId)

    # Check if the reactor is the publisher i.e. author of the lottery message
    if userId != getLottery(db, msgId)[0]:
        await member.send(languageConfig['lottery']['onlyPublisherCanOpen'])
        await message.remove_reaction(emoji, member)
        return

    # check if the lottery is closed
    if isOpen == 1:
        await message.channel.send(languageConfig['lottery']['lotteryClosed'])
        return

    # Check if enough people have participated
    if len(recipientIdList) < quantity:
        await message.channel.send(languageConfig['lottery']['notEnoughPeople'])
        await message.remove_reaction(emoji, member)
        return

    awardedUsers = random.sample(recipientIdList, quantity)
    awardedUsernameString = ""
    for awardedUser in awardedUsers:
        fetchedUser = await self.fetch_user(awardedUser)
        awardedUsernameString += fetchedUser.mention + "\n"

    publisher: User = await self.fetch_user(lotteryInfo[0])
    embedLotteryMessage = embedLib.lotteryResult.getEmbed(awardedUsernameString, publisher, reward)
    await message.channel.send(embed=embedLotteryMessage)
    updateLottery(db, msgId, isOpen=1)
    return
