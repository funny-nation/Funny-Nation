import client from '../../../client'
import { Interaction, MessageActionRow, MessageButton } from 'discord.js'
import { DBGuild } from '../../../models/DBGuild'
import getDBGuild from '../../../models/DBGuild/getDBGuild'
import getLanguage from '../../../language/getLanguage'
import getLanguageSettingMessageActionRow from './factories/get-language-setting-message-action-row'
import getTimeZoneSettingMessageActionRow from './factories/get-time-zone-setting-message-action-row'

/**
 * Listener for creating
 */
client.on('interactionCreate', async (interaction: Interaction) => {
  if (
    !interaction.isCommand() ||
    interaction.guild === null
  ) return

  const dbGuild: DBGuild = await getDBGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  if (interaction.commandName !== language.setGuildProfile.command || interaction.options.getSubcommand() !== 'lt') return

  const languageSettingRow = getLanguageSettingMessageActionRow(dbGuild.languageInGuild)

  const timeZoneSettingRow = getTimeZoneSettingMessageActionRow(dbGuild.languageInGuild, dbGuild.timeZone)

  const closeButton = new MessageActionRow()
    .addComponents([
      new MessageButton()
        .setCustomId('LanguageTimeZoneSettingCloseMenuButton')
        .setLabel('Close')
        .setStyle('SECONDARY')
    ])

  await interaction.reply({
    content: language.setGuildProfile.title,
    components: [languageSettingRow, timeZoneSettingRow, closeButton]
  })
})
