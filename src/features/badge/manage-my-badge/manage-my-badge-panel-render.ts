import { DBMemberBadge } from '../../../models/db-badge'
import { MessageActionRow, MessageButton } from 'discord.js'

const manageMyBadgePanelRender = async (userID: string, guildID: string): Promise<MessageActionRow[] | null> => {
  const memberBadges = await DBMemberBadge.fetchBadgesByMember(userID, guildID)
  if (memberBadges.length === 0) {
    return null
  }
  const mars: MessageActionRow[] = []
  for (const memberBadge of memberBadges) {
    const dbBadge = await memberBadge.getDBBadge()
    if (!dbBadge) {
      await memberBadge.remove()
      continue
    }
    const mar = new MessageActionRow()
    const emojiID = await dbBadge.getEmojiID()
    mar.addComponents([
      new MessageButton()
        .setEmoji(emojiID)
        .setLabel(`${dbBadge.badgeData.name} - expire in ${memberBadge.data.expiredAt.toLocaleDateString()}`)
        .setStyle('SUCCESS')
        .setCustomId('badgeAutoRenewToggleButton')
        .setDisabled(true),
      new MessageButton()
        .setLabel(memberBadge.data.autoRenew ? 'Auto-Renew - ON' : 'Auto-Renew - OFF')
        .setStyle(memberBadge.data.autoRenew ? 'SUCCESS' : 'SECONDARY')
        .setCustomId(`badgeAutoRenewToggleButton:${dbBadge.badgeData.id}`)
    ])
    mars.push(mar)
  }
  return mars
}

export { manageMyBadgePanelRender }
