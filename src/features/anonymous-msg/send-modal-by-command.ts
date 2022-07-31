import { client } from '../../client'
import { Interaction, MessageActionRow, Modal, ModalActionRowComponent, TextInputComponent } from 'discord.js'
import { TextInputStyles } from 'discord.js/typings/enums'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return

  if (interaction.commandName !== 'anonymous') return

  if (!interaction.guildId) return

  const dbGuild = await getDbGuild(interaction.guildId)
  const language = getLanguage(dbGuild.languageInGuild)
  const modal = new Modal()
    .setTitle(language.anonymousMsg.modal.title)
    .setCustomId('anonymousMessageModal')
    .addComponents(
      new MessageActionRow<ModalActionRowComponent>()
        .addComponents(
          new TextInputComponent()
            .setCustomId('input')
            .setLabel(language.anonymousMsg.modal.label)
            .setStyle(TextInputStyles.PARAGRAPH)
            .setRequired(true)
            .setMaxLength(255)
        ))
  await interaction.showModal(modal)
})
