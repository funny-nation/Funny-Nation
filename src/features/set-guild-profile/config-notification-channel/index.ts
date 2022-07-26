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
      interaction.commandName !== language.setGuildProfile.command ||
      interaction.options.getSubcommand() !== 'notification'
    ) return

    const notificationChannel = interaction.options.getChannel('channel')

    if (notificationChannel === null) return

    if (!await isAdmin(interaction.member)) {
      await interaction.reply('You don\'t have permission')
    }

    await dbGuild.setNotificationChannelID(notificationChannel.id)
    await interaction.reply(`Notification channel has changed to "${notificationChannel.name}"`)
  } catch (e) {
    console.log(e)
    logger.error('Error when someone change the notification channel')
  }
})
