import { DBGift } from '../../../models/db-gift/creat-gift'
import { updateGiftToOption } from '../helper/update-gift-to-option'
import { ModalSubmitInteraction } from 'discord.js'
import { Language } from '../../../language'
import { DBGuild } from '../../../models'
import { replyOnlyInteractorCanSee } from '../../../utils'

const submitModal = async (interaction: ModalSubmitInteraction, language: Language, dbGuild: DBGuild) => {
  if (!interaction.isModalSubmit()) return
  if (interaction.guild === null) return
  if (interaction.customId !== 'giftCreateModal') return

  // save gift info
  const giftName = interaction.fields.getField('giftNameInput').value
  const giftPrice = Number(interaction.fields.getField('priceInput').value)

  if (isNaN(giftPrice)) {
    await replyOnlyInteractorCanSee(interaction, 'Price must be a number')
    return
  }
  const giftEmoji = interaction.fields.getField('emojiInput').value
  const giftDesc = interaction.fields.getField('giftDesc').value
  const giftAnnouncement = interaction.fields.getField('giftAnnouncement').value
  const gift = await DBGift.createNewGift(giftName, giftEmoji, giftPrice, giftDesc, giftAnnouncement, interaction.guild.id || '')
  // bot reply
  if (!gift) {
    await replyOnlyInteractorCanSee(interaction, 'Gift existed')
    return
  }
  // update gift to option
  const guildId = dbGuild.id
  const giftList = await DBGift.getGiftList(guildId)
  await updateGiftToOption(giftList, interaction, language)
  await replyOnlyInteractorCanSee(interaction, 'Gift created')
}

export { submitModal }
