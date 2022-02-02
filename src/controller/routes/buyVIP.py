from discord import Client, Message, TextChannel, Member, File
from pymysql import Connection

from src.utils.readConfig import getLanguageConfig, getVipTagsConfig, getCashFlowMsgConfig

from src.model.userManagement import getUser, editUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow


async def buyVIP(self: Client, message: Message, db: Connection, annocementChannel: TextChannel, vipRoles: dict):
    user: Member = message.author
    userInfo: tuple = getUser(db, user.id)
    languageConfig = getLanguageConfig()
    if userInfo is None:
        returnMsg = str(languageConfig['vip']['notEnoughMoney'])\
            .replace('?@user', user.display_name)
        await message.channel.send(returnMsg)
        return

    vipConfig = getVipTagsConfig()
    cashFlowMsgConfig = getCashFlowMsgConfig()
    nextVIPLevel = userInfo[5] + 1

    if nextVIPLevel not in vipRoles:
        returnMsg = str(languageConfig['vip']['youAreInTheHighestLevel'])\
            .replace('?@user', user.display_name)
        await message.channel.send(returnMsg)
        return

    vipDetails = vipConfig[str(nextVIPLevel)]

    price = int(vipDetails['price'])

    if userInfo[1] < price:
        returnMsg = str(languageConfig['vip']['notEnoughMoney'])\
            .replace('?@user', user.display_name)
        await message.channel.send(returnMsg)
        return

    databaseResult = True
    databaseResult = databaseResult and addMoneyToUser(db, user.id, -price)
    databaseResult = databaseResult and addNewCashFlow(db, user.id, -price, cashFlowMsgConfig['vip']['buyVIP'])
    databaseResult = databaseResult and editUser(db, userID=user.id, vipLevel=nextVIPLevel)

    if not databaseResult:
        returnMsg = str(languageConfig['error']['dbError'])
        await message.channel.send(returnMsg)
        return

    vipRole = vipRoles[nextVIPLevel]
    try:
        await user.add_roles(vipRole)
    except Exception as err:
        msg = str(languageConfig['vip']['askAdminForHelp'])\
            .replace('?@user', user.display_name)
        await message.channel.send(msg)

    annocementMsg = languageConfig['vip']['announcement']\
        .replace('?@user', user.display_name)\
        .replace('?@levelName', vipDetails['name'])
    replyMsg = languageConfig['vip']['purchaseSuccess']\
        .replace('?@user', user.display_name)


    await annocementChannel.send(annocementMsg)
    await message.channel.send(replyMsg)

    if vipConfig.has_option(str(nextVIPLevel), 'img'):
        await annocementChannel.send(file=File(vipDetails['img']))


