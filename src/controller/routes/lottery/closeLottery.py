from discord import Client, Message, Member, PartialEmoji
from pymysql import Connection
from src.model.lotteryManagement import updateLottery, getLottery, getLotteryRecipient
from src.model.userManagement import addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
from src.utils.readConfig import getLanguageConfig, getCashFlowMsgConfig

languageConfig = getLanguageConfig()
cashflowConfig = getCashFlowMsgConfig()


async def closeLottery(self: Client, db: Connection, userId: int, msgId: int, member: Member, channelId: int, emoji: PartialEmoji):
    channel = self.get_channel(channelId)
    message: Message = await channel.fetch_message(msgId)

    lotteryInfo: tuple = getLottery(db, msgId)
    lotteryPrice: int = lotteryInfo[4]
    isOpen: int = lotteryInfo[5]

    # Check if the emoji reactor is the publisher
    if userId != getLottery(db, msgId)[0]:
        await member.send(languageConfig['lottery']['onlyPublisherCanClose'])
        await message.remove_reaction(emoji, member)
        return

    # check if the lottery is closed
    if isOpen == 1:
        await message.channel.send(languageConfig['lottery']['lotteryClosed'])
        return

    systemError = str(languageConfig['error']["dbError"])
    response: bool = updateLottery(db, msgId, isOpen=1)

    if response is False:
        await message.channel.send(systemError)
        return

    recipientIdList: list = list(map(lambda x: x[0], getLotteryRecipient(db, msgId)))
    for recipientId in recipientIdList:
        addMoneyToUser(db, recipientId, lotteryPrice)
        addNewCashFlow(db, recipientId, lotteryPrice, cashflowConfig['lottery']['withdrawnLottery'])
    return
