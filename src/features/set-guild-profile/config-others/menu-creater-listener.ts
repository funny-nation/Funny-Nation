import { client } from '../../../client'
import { GuildMember, Interaction, MessageActionRow, MessageButton } from 'discord.js'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'
import { getLanguageSettingMessageActionRow, getTimeZoneSettingMessageActionRow } from './factories'
import { isAdmin } from '../../../utils'
import { logger } from '../../../logger'

/**
 * Listener for creating
 */
client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (
      !interaction.isCommand() ||
      interaction.guild === null ||
      !(interaction.member instanceof GuildMember)
    ) return

    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (
      interaction.commandName !== language.setGuildProfile.commands.name ||
      interaction.options.getSubcommand() !== language.setGuildProfile.commands.subcommand.setOthers.name
    ) return

    if (!await isAdmin(interaction.member)) {
      await interaction.reply(language.setGuildProfile.invalidAccess)
    }

    const languageSettingRow = getLanguageSettingMessageActionRow(dbGuild.languageInGuild)

    const timeZoneSettingRow = getTimeZoneSettingMessageActionRow(dbGuild.languageInGuild, dbGuild.timeZone)

    const closeButton = new MessageActionRow()
      .addComponents([
        new MessageButton()
          .setCustomId('LanguageTimeZoneSettingCloseMenuButton')
          .setLabel(language.setGuildProfile.close)
          .setStyle('SECONDARY')
      ])

    await interaction.reply({
      content: language.setGuildProfile.otherSettingMenu.title,
      components: [languageSettingRow, timeZoneSettingRow, closeButton]
    })
  } catch (e) {
    console.log(e)
    logger.error('Error when configure guild others profile menu is created')
  }
})
