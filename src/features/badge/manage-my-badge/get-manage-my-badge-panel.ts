import { CommandInteraction } from 'discord.js'
import { manageMyBadgePanelRender } from './manage-my-badge-panel-render'
import { replyOnlyInteractorCanSee, replyThenDelete } from '../../../utils'

const getManageMyBadgePanel = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  const user = interaction.user
  if (!guild || !user) return
  const panel = await manageMyBadgePanelRender(user.id, guild.id)
  if (!panel) {
    replyOnlyInteractorCanSee(interaction, 'You do not have any badges in this server')
    return
  }
  replyThenDelete(interaction, {
    components: panel
  })
}

export { getManageMyBadgePanel }
