import { isBotStarted } from '../../bot'
import { DBBadge, DBMemberBadge } from '../../models/db-badge'
import { addDbCoinTransfer, getDbMember } from '../../models'
import { logger } from '../../logger'
import { client } from '../../client'

const badgeExpCheckIntervalInMS = 1000 * 60 * 60
setInterval(() => {
  if (isBotStarted()) {
    try {
      badgeExpirationDetector()
    } catch (e) {
      console.log(e)
      logger.error('Error in badgeExpirationDetector')
    }
  }
}, badgeExpCheckIntervalInMS)

const badgeExpirationDetector = async () => {
  const expiredMemberBadges = await DBMemberBadge.fetchExpiredBadges()
  logger.verbose(`There are ${expiredMemberBadges.length} expired badges`)
  for (const expiredMemberBadge of expiredMemberBadges) {
    let guild
    let member
    try {
      guild = await client.guilds.fetch(expiredMemberBadge.data.guildID)
      member = await guild.members.fetch(expiredMemberBadge.data.userID)
    } catch (e) {
      await expiredMemberBadge.remove()
      continue
    }
    const dbMember = await getDbMember(expiredMemberBadge.data.userID, expiredMemberBadge.data.guildID)
    const dbBadge = await DBBadge.fetchByID(expiredMemberBadge.data.badgeID)
    if (!dbBadge) {
      await expiredMemberBadge.remove()
      return
    }
    if (
      !expiredMemberBadge.data.autoRenew ||
      dbMember.coinBalanceInGuild < dbBadge.badgeData.price) {
      logger.verbose(`Badge "${dbBadge.badgeData.name}" has been removed from user "${member}" due to expiration. `)
      await expiredMemberBadge.remove()
      try {
        await member.roles.remove(dbBadge.badgeData.roleIDRelated)
      } catch (e) {
        logger.info('Role remove for badge expiration error')
      }
      continue
    }
    await dbMember.reduceCoins(Number(dbBadge.badgeData.price))
    await addDbCoinTransfer(dbMember.userID, dbMember.guildID, Number(dbBadge.badgeData.price), null, '', 'buyBadge')
    await expiredMemberBadge.extend()
    logger.verbose(`Badge "${dbBadge.badgeData.name}" renewed for user "${dbMember.userID}"`)
  }
}
