import { MessageActionRow, Modal, ModalActionRowComponent, TextInputComponent } from 'discord.js'
import { TextInputStyles } from 'discord.js/typings/enums'
import { LanguageEnum } from '../../../models'
import { getLanguage } from '../../../language'

const getSuperUserNotificationModal = (customID: string, targetLanguage: LanguageEnum = 'English'): Modal => {
  const language = getLanguage(targetLanguage)
  const modal = new Modal()
    .setTitle(language.notification)
    .setCustomId(customID)

  modal.addComponents(
    new MessageActionRow<ModalActionRowComponent>()
      .addComponents(
        new TextInputComponent()
          .setCustomId('input')
          .setLabel('Message')
          .setStyle(TextInputStyles.PARAGRAPH)
      )
  )

  if (targetLanguage) {
    modal.addComponents(
      new MessageActionRow<ModalActionRowComponent>()
        .addComponents(
          new TextInputComponent()
            .setCustomId('language')
            .setLabel('Guilds with this language could receive')
            .setValue(targetLanguage)
            .setStyle(TextInputStyles.SHORT)
        )
    )
  }
  return modal
}

export { getSuperUserNotificationModal }
