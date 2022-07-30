import { client } from '../../client'
import { Interaction, MessageActionRow, Modal, ModalActionRowComponent, TextInputComponent } from 'discord.js'
import { TextInputStyles } from 'discord.js/typings/enums'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return

  if (interaction.commandName !== 'anonymous') return

  const modal = new Modal()
    .setTitle('Anonymous Message')
    .setCustomId('anonymousMessageModal')
    .addComponents(
      new MessageActionRow<ModalActionRowComponent>()
        .addComponents(
          new TextInputComponent()
            .setCustomId('input')
            .setLabel('Message')
            .setStyle(TextInputStyles.PARAGRAPH)
            .setRequired(true)
            .setMaxLength(255)
        ))
  await interaction.showModal(modal)
})
