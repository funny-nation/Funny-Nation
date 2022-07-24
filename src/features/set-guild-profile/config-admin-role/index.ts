import client from '../../../client'
import { Interaction } from 'discord.js'
import { DBGuild } from '../../../models/DBGuild'
import { Language } from '../../../language'
import getLanguage from '../../../language/getLanguage'
import logger from '../../../logger'
import getDBGuild from '../../../models/DBGuild/getDBGuild'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand() || interaction.guild === null) return

    const dbGuild: DBGuild = await getDBGuild(interaction.guild.id)
    const language: Language = getLanguage(dbGuild.languageInGuild)
    const roleFromOption = interaction.options.getRole('role')
    if (interaction.commandName !== language.setGuildProfile.command || interaction.options.getSubcommand() !== 'admin' || roleFromOption === null) return
    await dbGuild.setAdministratorRoleID(roleFromOption.id)
    await interaction.reply(`Administrator role has changed to ${roleFromOption.name}`)
  } catch (e) {
    console.log(e)
    logger.error('Error when someone change the administrator role')
  }
})
