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
      !(interaction.member instanceof GuildMember)
    ) return

    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language: Language = getLanguage(dbGuild.languageInGuild)

    if (
      interaction.commandName !== language.setGuildProfile.commands.name ||
      interaction.options.getSubcommand() !== language.setGuildProfile.commands.subcommand.setAnnouncement.name
    ) return

    const announcementChannel = interaction.options.getChannel(language.setGuildProfile.commands.subcommand.setAnnouncement.optionName)

    if (announcementChannel === null) return

    if (!await isAdmin(interaction.member)) {
      await interaction.reply(language.setGuildProfile.invalidAccess)
    }

    await dbGuild.setAnnouncementChannelID(announcementChannel.id)
    await interaction.reply(language.setGuildProfile.successMsg.setAnnouncementChannel(announcementChannel.name))
  } catch (e) {
    console.log(e)
    logger.error('Error when someone change the announcement channel')
  }
})
