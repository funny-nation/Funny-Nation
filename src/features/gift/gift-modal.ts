import { client } from '../../client'
import {
  GuildMember,
  Interaction,
  MessageActionRow,
  Modal,
  ModalActionRowComponent,
  TextInputComponent
} from 'discord.js'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'
import { logger } from '../../logger'
import { isAdmin } from '../../utils'
import { DBGift } from '../../models/db-gift/creat-gift'
import { updateGiftToOption } from './helper/update-gift-to-option'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand() || !interaction.guild) return
    // localization
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = await getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.gift.command.name) return
    // if (interaction.options.getSubcommand() !== language.gift.command.createGift.name) return
    if (!interaction.member) return
    if (!(interaction.member instanceof GuildMember)) return
    // verify admin user
    const isAdministrator = await isAdmin(interaction.member)
    if (!isAdministrator) {
      await interaction.reply({
        content: 'you are not administrator'
      })
      return
    }
    const giftName = interaction.options.getString(language.gift.command.createGift.stringOptionName)
    const giftEmoji = interaction.options.getString(language.gift.command.createGift.emojiOptionName)
    const giftPrice = interaction.options.getNumber(language.gift.command.createGift.numberOptionName)
    console.log('giftName', giftName, 'giftEmoji', giftEmoji, 'giftPrice', giftPrice)
    if (!giftName || !giftEmoji || !giftPrice) return
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
      .setMaxLength(20)
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
})
client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isModalSubmit()) return
    if (interaction.guild === null) return
    if (interaction.customId !== 'giftCreateModal') return

    // save gift info
    const giftName = interaction.fields.getField('giftNameInput').value
    const giftPrice = Number(interaction.fields.getField('priceInput').value)
    // localization
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = await getLanguage(dbGuild.languageInGuild)

    if (isNaN(giftPrice)) {
      await interaction.reply({
        content: 'Price must be a number'
      })
      return
    }
    const giftEmoji = interaction.fields.getField('emojiInput').value
    const giftDesc = interaction.fields.getField('giftDesc').value
    const giftAnnouncement = interaction.fields.getField('giftAnnouncement').value
    const gift = await DBGift.createNewGift(giftName, giftEmoji, giftPrice, giftDesc, giftAnnouncement, interaction.guild.id || '')
    // bot reply
    if (!gift) {
      await interaction.reply(
        {
          content: 'Gift existed'
        }
      )
      return
    }
    // update gift to option
    const guildId = dbGuild.id
    const giftList = await DBGift.getGiftList(guildId)
    const option = 'create'
    await updateGiftToOption(giftList, interaction, language, option)
    await interaction.reply({
      content: 'Gift created'
    })
  } catch (e) {
    console.log(e)
    logger.error('error occurs when executing feature/gift/gift-modal')
  }
})
