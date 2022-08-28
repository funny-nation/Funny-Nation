import { isBotStarted } from '../../bot'
import { DBBadge, DBMemberBadge } from '../../models/db-badge'
import { addDbCoinTransfer, getDbMember } from '../../models'
import { logger } from '../../logger'

const badgeExpCheckIntervalInMS = 10000
setInterval(() => {
  if (isBotStarted()) {
    badgeExpirationDetector()
  }
}, badgeExpCheckIntervalInMS)

const badgeExpirationDetector = async () => {
  const expiredMemberBadges = await DBMemberBadge.fetchExpiredBadges()
  logger.verbose(`There are ${expiredMemberBadges.length} expired badges`)
  for (const expiredMemberBadge of expiredMemberBadges) {
    if (!expiredMemberBadge.data.autoRenew) {
      logger.verbose(`Badge "${expiredMemberBadge.data.badgeID}" has been removed from user "${expiredMemberBadge.data.userID}" due to expiration. `)
      await expiredMemberBadge.remove()
      continue
    }
    const dbMember = await getDbMember(expiredMemberBadge.data.userID, expiredMemberBadge.data.guildID)
    const dbBadge = await DBBadge.fetchByID(expiredMemberBadge.data.badgeID)
    if (!dbBadge || dbMember.coinBalanceInGuild < dbBadge.badgeData.price) {
      logger.verbose(`Badge "${expiredMemberBadge.data.badgeID}" has been removed from user "${expiredMemberBadge.data.userID}" due to expiration and not affordable. `)
      await expiredMemberBadge.remove()
      continue
    }
    await dbMember.reduceCoins(Number(dbBadge.badgeData.price))
    await addDbCoinTransfer(dbMember.userID, dbMember.guildID, Number(dbBadge.badgeData.price), null, '', 'buyBadge')
    await expiredMemberBadge.extend()
    logger.verbose(`Badge "${dbBadge.badgeData.name}" renewed for user "${dbMember.userID}"`)
  }
}
