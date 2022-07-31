import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { getNickNameByUserId } from './user-id-nick-name-map'
import { getLanguage } from '../../language'
import { getDbGuild } from '../../models'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isModalSubmit()) return

  if (interaction.customId !== 'anonymousMessageModal') return

  if (!interaction.guildId) return

  const nickName = getNickNameByUserId(interaction.user.id)
  const anonymousContent = interaction.fields.getTextInputValue('input')

  if (!anonymousContent) return

  const dbGuild = await getDbGuild(interaction.guildId)
  const language = getLanguage(dbGuild.languageInGuild)
  await interaction.deferReply({ ephemeral: true })
  if (!interaction.channel) {
    await interaction.editReply(language.anonymousMsg.sendFailed)
    return
  }
  await interaction.channel.send({
    embeds: [
      new MessageEmbed()
        .setTitle(anonymousContent)
        .setFooter({
          text: language.anonymousMsg.anonymousMsgFrom(nickName)
        })
        .setColor('#FF99CC')
    ]
  })
  await interaction.editReply(language.anonymousMsg.sent)
})
