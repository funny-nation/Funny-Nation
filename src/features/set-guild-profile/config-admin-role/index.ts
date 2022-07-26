import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { DBGuild, getDbGuild } from '../../../models'
import { Language, getLanguage } from '../../../language'
import { logger } from '../../../logger'
import { isAdmin } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (
      !interaction.isCommand() ||
      interaction.guild === null ||
      interaction.member === null ||
      !(interaction.member instanceof GuildMember) ||
      interaction.commandName !== 'config'
    ) return

    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language: Language = getLanguage(dbGuild.languageInGuild)
    const roleFromOption = interaction.options.getRole('role')

    if (
      interaction.commandName !== language.setGuildProfile.command ||
      interaction.options.getSubcommand() !== 'admin' ||
      roleFromOption === null
    ) return
    if (!await isAdmin(interaction.member)) {
      await interaction.reply('You don\'t have permission')
    }

    await dbGuild.setAdministratorRoleID(roleFromOption.id)
    await interaction.reply(`Administrator role has changed to ${roleFromOption.name}`)
  } catch (e) {
    console.log(e)
    logger.error('Error when someone change the administrator role')
  }
})
