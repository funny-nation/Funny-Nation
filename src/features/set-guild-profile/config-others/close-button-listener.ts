import { client } from '../../../client'
import { GuildMember, Interaction, Message } from 'discord.js'
import { isAdmin } from '../../../utils'
import { logger } from '../../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (
      !interaction.isButton() ||
      interaction.customId !== 'LanguageTimeZoneSettingCloseMenuButton' ||
      interaction.member === null ||
      interaction.guild === null
    ) return

    if (
      !(interaction.member instanceof GuildMember) ||
      !(interaction.message instanceof Message)
    ) return

    if (!await isAdmin(interaction.member)) return

    await interaction.message.edit({
      content: '^_^',
      components: []
    })
  } catch (e) {
    console.log(e)
    logger.error('Error when closing configure other menu')
  }
})
