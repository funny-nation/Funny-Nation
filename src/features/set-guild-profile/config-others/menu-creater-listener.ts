import { client } from '../../../client'
import { GuildMember, Interaction, MessageActionRow, MessageButton } from 'discord.js'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'
import { getLanguageSettingMessageActionRow, getTimeZoneSettingMessageActionRow } from './factories'
import { isAdmin } from '../../../utils'

/**
 * Listener for creating
 */
client.on('interactionCreate', async (interaction: Interaction) => {
  if (
    !interaction.isCommand() ||
    interaction.guild === null ||
    !(interaction.member instanceof GuildMember)
  ) return

  const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  if (interaction.commandName !== language.setGuildProfile.command || interaction.options.getSubcommand() !== 'others') return

  if (!await isAdmin(interaction.member)) {
    await interaction.reply('You don\'t have permission')
  }

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
