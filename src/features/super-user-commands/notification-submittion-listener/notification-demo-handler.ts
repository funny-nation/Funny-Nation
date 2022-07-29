import { MessageEmbed, ModalSubmitInteraction } from 'discord.js'

const notificationDemoHandler = async (interaction: ModalSubmitInteraction) => {
  const notificationMsg = interaction.fields.getTextInputValue('input')
  await interaction.reply({
    embeds: [
      new MessageEmbed()
        .setColor('#FF99CC')
        .setTitle('Notification')
        .setDescription(notificationMsg)
    ]
  })
}

export { notificationDemoHandler }
