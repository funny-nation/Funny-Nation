from discord import Client, Member, Message, PartialEmoji
from pymysql import Connection

from src.model.cashFlowManagement import addNewCashFlow
from src.model.lotteryManagement import addNewLotteryRecipient, getLottery, getLotteryRecipient
from src.model.userManagement import addMoneyToUser, getUser
from src.utils.readConfig import getCashFlowMsgConfig, getLanguageConfig

cashflowMsgConfig = getCashFlowMsgConfig()
languageConfig = getLanguageConfig()


async def joinLottery(self: Client, db: Connection, recipientId: int, msgId: int, member: Member, channelId: int, emoji: PartialEmoji):
    lotteryInfo: tuple = getLottery(db, msgId)
    lotteryRecipients: list = list(map(lambda x: x[0], getLotteryRecipient(db, msgId)))
    price: int = lotteryInfo[4]

    if getUser(db, recipientId)[1] < price:
        notEnoughMoneyMessage: str = languageConfig['lottery']['notEnoughMoney'].replace('?@user_name', member.mention)
        await member.send(notEnoughMoneyMessage)
        channel = self.get_channel(channelId)
        message: Message = await channel.fetch_message(msgId)
        await message.remove_reaction(emoji, member)
        return

    if recipientId in lotteryRecipients:
        alreadyParticipated: str = languageConfig['lottery']['alreadyParticipated'].replace('?@user_name', member.mention)
        await member.send(alreadyParticipated)
        return

    response: bool = addNewLotteryRecipient(db, recipientId, msgId)

    if response is True:
        dmMessage: str = languageConfig['lottery']['joinedLottery'].replace('?@user_name', member.mention)
        addMoneyToUser(db, member.id, -price)
        addNewCashFlow(db, member.id, -price, cashflowMsgConfig['lottery']['participatedLottery'])
        await member.send(dmMessage)
