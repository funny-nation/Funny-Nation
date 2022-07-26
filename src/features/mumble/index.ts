import { client } from '../../client'
import { Interaction, User } from 'discord.js'
import { getLanguage } from '../../language'
import { getDbGuild, DBGuild } from '../../models'
import { logger } from '../../logger'

/**
 * This function will listen to the contextMenu event
 * @param interaction
 * @returns null
 */

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isUserContextMenu() || interaction.guild === null) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.mumble.mumble) return
    const targetUser: User = interaction.targetUser
    await interaction.reply(language.mumble.language(`<@${interaction.user.id}>`, `<@${targetUser.id}>`))
  } catch (e) {
    console.log(e)
    logger.error('Error when someone interact ContextManu')
  }
})
