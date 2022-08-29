import { CommandInteraction } from 'discord.js'
import { manageMyBadgePanelRender } from './manage-my-badge-panel-render'
import { replyOnlyInteractorCanSee, replyThenDelete } from '../../../utils'
import { getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

const getManageMyBadgePanel = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  const user = interaction.user
  if (!guild || !user) return
  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge
  const panel = await manageMyBadgePanelRender(user.id, guild.id)
  if (!panel) {
    replyOnlyInteractorCanSee(interaction, language.youDontHaveAnyBadgeInThisServer)
    return
  }
  replyThenDelete(interaction, {
    components: panel
  })
}

export { getManageMyBadgePanel }
