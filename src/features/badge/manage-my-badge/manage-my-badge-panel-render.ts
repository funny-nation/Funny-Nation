import { DBMemberBadge } from '../../../models/db-badge'
import { MessageActionRow, MessageButton } from 'discord.js'
import { getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

const manageMyBadgePanelRender = async (userID: string, guildID: string): Promise<MessageActionRow[] | null> => {
  const dbGuild = await getDbGuild(guildID)
  const language = getLanguage(dbGuild.languageInGuild).badge
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
        .setLabel(language.badgeExpireIn(dbBadge.badgeData.name, memberBadge.data.expiredAt.toLocaleDateString()))
        .setStyle('SUCCESS')
        .setCustomId(String(dbBadge.badgeData.id))
        .setDisabled(true),
      new MessageButton()
        .setLabel(memberBadge.data.autoRenew ? language.autoRenewOn : language.autoRenewOff)
        .setStyle(memberBadge.data.autoRenew ? 'SUCCESS' : 'SECONDARY')
        .setCustomId(`badgeAutoRenewToggleButton:${dbBadge.badgeData.id}`)
    ])
    mars.push(mar)
  }
  return mars
}

export { manageMyBadgePanelRender }
