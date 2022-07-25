import client from '../../../client'
import { GuildMemberRoleManager, Interaction, Message, Permissions } from 'discord.js'
import getDBGuild from '../../../models/DBGuild/getDBGuild'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (
    !interaction.isButton() ||
    interaction.customId !== 'LanguageTimeZoneSettingCloseMenuButton' ||
    interaction.member === null ||
    interaction.guild === null
  ) return

  if (
    !(interaction.member.roles instanceof GuildMemberRoleManager) ||
    !(interaction.member.permissions instanceof Permissions) ||
    !(interaction.message instanceof Message)
  ) return

  const dbGuild = await getDBGuild(interaction.guild.id)
  let hasPermission = interaction.member.permissions.has('ADMINISTRATOR')
  if (dbGuild.administratorRoleID !== null) {
    hasPermission = hasPermission || interaction.member.roles.cache.has(dbGuild.administratorRoleID)
  }
  if (!hasPermission) {
    await interaction.reply('You don\'t have permission')
  }

  await interaction.message.edit({
    content: 'Closed',
    components: []
  })
})
