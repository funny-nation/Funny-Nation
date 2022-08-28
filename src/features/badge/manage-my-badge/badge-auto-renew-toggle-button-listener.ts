import { ButtonInteraction } from 'discord.js'
import { DBMemberBadge } from '../../../models/db-badge'
import { replyOnlyInteractorCanSee } from '../../../utils'
import { manageMyBadgePanelRender } from './manage-my-badge-panel-render'
import { logger } from '../../../logger'
import { getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

const badgeAutoRenewToggleButtonListener = async (interaction: ButtonInteraction) => {
  const customIDArr = interaction.customId.split(':')
  const user = interaction.user
  const guild = interaction.guild
  if (
    customIDArr.length !== 2 ||
    !guild
  ) return

  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge

  const badgeID = customIDArr[1]

  const dbMemberBadge = await DBMemberBadge.fetchBadge(Number(badgeID), user.id, guild.id)

  if (!dbMemberBadge) {
    replyOnlyInteractorCanSee(interaction, language.badgeNotFound)
    return
  }

  await dbMemberBadge.toggleAutoRenew()
  logger.verbose(`User "${user}" toggle his/her auto renew setting to ${dbMemberBadge.data.autoRenew}`)
  const panel = await manageMyBadgePanelRender(user.id, guild.id)
  if (!panel) {
    await interaction.update({})
    return
  }
  replyOnlyInteractorCanSee(interaction, {
    components: panel
  })
}

export { badgeAutoRenewToggleButtonListener }
