import { client } from '../../../client'
import { Interaction, MessageActionRow, Modal, ModalActionRowComponent, TextInputComponent } from 'discord.js'
import { TextInputStyles } from 'discord.js/typings/enums'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return

  if (interaction.commandName !== 'dealer') return

  if (interaction.options.getSubcommand() !== 'custom-single') return

  const modal = new Modal()
    .setTitle('发牌器')
    .setCustomId('dealerModalSubmission')
    .addComponents(
      new MessageActionRow<ModalActionRowComponent>()
        .addComponents(
          new TextInputComponent()
            .setCustomId('input')
            .setLabel('Roles')
            .setRequired(true)
            .setStyle(TextInputStyles.PARAGRAPH)
        )
    )
  await interaction.showModal(modal)
})
