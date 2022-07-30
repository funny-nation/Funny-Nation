import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { getNickNameByUserId } from './user-id-nick-name-map'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isModalSubmit()) return

  if (interaction.customId !== 'anonymousMessageModal') return

  const nickName = getNickNameByUserId(interaction.user.id)
  const anonymousContent = interaction.fields.getTextInputValue('input')

  if (!anonymousContent) return

  await interaction.deferReply({ ephemeral: true })
  if (!interaction.channel) {
    await interaction.editReply('failed')
    return
  }
  await interaction.channel.send({
    embeds: [
      new MessageEmbed()
        .setTitle(anonymousContent)
        .setDescription(`From ${nickName}`)
        .setColor('#FF99CC')
    ]
  })
  await interaction.editReply('sent')
})
