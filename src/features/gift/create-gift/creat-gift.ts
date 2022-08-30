import {
  CommandInteraction,
  GuildMember,
  MessageActionRow,
  Modal,
  ModalActionRowComponent,
  TextInputComponent
} from 'discord.js'
import { Language } from '../../../language'
import { getEmojiIDFromStr, isAdmin, replyOnlyInteractorCanSee } from '../../../utils'
import { logger } from '../../../logger'

const createGift = async (interaction: CommandInteraction, language: Language) => {
  // create gift
  try {
    if (!interaction.member) return
    if (!(interaction.member instanceof GuildMember)) return
    // verify admin user
    const isAdministrator = await isAdmin(interaction.member)
    if (!isAdministrator) {
      await replyOnlyInteractorCanSee(interaction, 'you are not administrator')
      return
    }
    const giftName = interaction.options.getString(language.gift.command.createGift.stringOptionName)
    const giftEmoji = interaction.options.getString(language.gift.command.createGift.emojiOptionName)
    const giftPrice = interaction.options.getNumber(language.gift.command.createGift.numberOptionName)

    if (!giftName || !giftEmoji || !giftPrice) return
    const emojiID = getEmojiIDFromStr(giftEmoji)
    if (!emojiID) {
      await replyOnlyInteractorCanSee(interaction, language.gift.emojiInvalid)
    }
    // create gift modal
    const modal = new Modal()
      .setTitle(language.gift.modal.titleName)
      .setCustomId('giftCreateModal')
    const giftComponent = new TextInputComponent()
      .setValue(giftName)
      .setCustomId('giftNameInput')
      .setLabel(language.gift.modal.giftLabelName)
      .setStyle('SHORT')
      .setMaxLength(20)
      .setRequired(true)
    const emojiComponent = new TextInputComponent()
      .setValue(giftEmoji)
      .setLabel(language.gift.modal.emojiLabelName)
      .setCustomId('emojiInput')
      .setStyle('SHORT')
      .setMaxLength(256)
      .setRequired(true)
    const giftPriceComponent = new TextInputComponent()
      .setValue(giftPrice.toString())
      .setLabel(language.gift.modal.priceLabelName)
      .setCustomId('priceInput')
      .setStyle('SHORT')
      .setMaxLength(20)
      .setRequired(true)
    const giftDescComponent = new TextInputComponent()
      .setLabel(language.gift.modal.giftDescLabelName)
      .setStyle('PARAGRAPH')
      .setCustomId('giftDesc')
      .setMaxLength(2048)
      .setRequired(true)
    const giftAnnouncementComponent = new TextInputComponent()
      .setLabel(language.gift.modal.giftAnnounceLabelName)
      .setStyle('PARAGRAPH')
      .setCustomId('giftAnnouncement')
      .setMaxLength(2048)
      .setRequired(true)

    modal.addComponents(
      new MessageActionRow<ModalActionRowComponent>().addComponents(giftComponent),
      new MessageActionRow<ModalActionRowComponent>().addComponents(emojiComponent),
      new MessageActionRow<ModalActionRowComponent>().addComponents(giftPriceComponent),
      new MessageActionRow<ModalActionRowComponent>().addComponents(giftDescComponent),
      new MessageActionRow<ModalActionRowComponent>().addComponents(giftAnnouncementComponent)
    )
    await interaction.showModal(modal)
  } catch (e) {
    console.log(e)
    logger.error('error occurs when executing feature/gift/gift-modal')
  }
}

export { createGift }
