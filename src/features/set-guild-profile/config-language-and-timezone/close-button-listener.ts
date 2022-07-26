import { client } from '../../../client'
import { GuildMember, Interaction, Message } from 'discord.js'
import { isAdmin } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
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

  if (!await isAdmin(interaction.member)) {
    await interaction.reply('You don\'t have permission')
  }

  await interaction.message.edit({
    content: 'Closed',
    components: []
  })
})
