import { client } from '../../../client'
import { Interaction } from 'discord.js'
import { getTabletop } from './storage'
import { getLanguage } from '../../../language'
import { DBGuild, getDbGuild } from '../../../models'
import { cleanTable } from './utils/cleanTable'
import { logger } from '../../../logger'
import { replyOnlyInteractorCanSee } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isButton()) return
    if (interaction.customId !== 'roleAssignCloseButton') return
    const tabletop = getTabletop(interaction.channelId)
    if (!interaction.guild) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (!tabletop) {
      await cleanTable(interaction)
      return
    }
    if (tabletop.owner !== interaction.member) {
      if (interaction.channel) {
        replyOnlyInteractorCanSee(interaction, interaction.user.username + language.tabletopRoleAssign.cannotCloseGame)
        // await interaction.reply(interaction.user.username + language.tabletopRoleAssign.cannotCloseGame)
      }
      return
    }
    tabletop.destroy()
    await cleanTable(interaction)
  } catch (e) {
    console.log(e)
    logger.error('Error when a user using close button')
  }
})
