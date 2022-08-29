import { addDbCoinTransfer, DBGuild, getDbMember } from '../../../models'
import { Language } from '../../../language'
import { client } from '../../../client'
import { DBGift } from '../../../models/db-gift/creat-gift'
import { expAdjustment } from '../helper/exp-adjustment'
import { createInventory } from '../../../models/db-inventory'
import moment from 'moment'
import { CommandInteraction, MessageEmbed } from 'discord.js'
import { getEmojiIDFromStr, replyOnlyInteractorCanSee } from '../../../utils'

const sendGift = async (interaction: CommandInteraction, language: Language, dbGuild: DBGuild) => {
  const giftID = interaction.options.getString(language.gift.command.sendGift.stringOptionName)
  const receiver = interaction.options.getUser(language.gift.command.sendGift.userOptionName)

  if (!giftID || !receiver) return

  if (!client.user) return
  if (receiver.id === client.user.id) {
    await replyOnlyInteractorCanSee(interaction, language.gift.errorHandler.botReply)
    return
  }
  if (receiver.id === interaction.user.id) {
    await replyOnlyInteractorCanSee(interaction, language.gift.errorHandler.userReply)
    return
  }
  // query sender and receiver from db with ids
  if (!interaction.guild) return
  const senderInfo = await getDbMember(interaction.user.id, interaction.guild.id)
  const receiverInfo = await getDbMember(receiver.id, interaction.guild.id)
  // get gift info
  const giftName = interaction.options.getString(language.gift.command.sendGift.stringOptionName)
  if (!giftName) return
  const gift = await DBGift.getGift(giftName, dbGuild.id)
  if (!gift) return
  const price = Number(gift.giftData.price)
  if (senderInfo.coinBalanceInGuild < price) {
    await replyOnlyInteractorCanSee(interaction, language.gift.hasEnoughMoney)
    return
  }
  // adjust money and exp between gift sender and receiver after gift sent
  await senderInfo.reduceCoins(price)
  await senderInfo.addMemberExperience(expAdjustment(price).senderExp)
  await receiverInfo.addMemberExperience(expAdjustment(price).receiverExp)
  await addDbCoinTransfer(senderInfo.userID, interaction.guild.id, price, null, '', 'sendGift')
  // create inventory
  await createInventory(giftName, price, 'gift', receiver.id, moment().utc().toDate(), interaction.guild.id)

  await replyOnlyInteractorCanSee(interaction, 'gift sent')
  const emojiStr = gift.giftData.emoji
  const emojiId = getEmojiIDFromStr(emojiStr)
  if (!emojiId) return

  let emoji
  try {
    emoji = await interaction.guild.emojis.fetch(emojiId)
  } catch (e) {
    await replyOnlyInteractorCanSee(interaction, language.gift.emojiDoesNotExistHere)
  }
  if (!emoji) {
    await replyOnlyInteractorCanSee(interaction, language.gift.emojiInvalid)
    return
  }
  const embed = new MessageEmbed()
    .setThumbnail(emoji.url)
    .setDescription('')
    .setColor('#FF99CC')
  if (!interaction.channel) return
  if (!dbGuild.announcementChannelID) {
    interaction.channel.send({
      content: `<@${senderInfo.userID}>给老板<@${receiverInfo.userID}>送了${interaction.options.getString(language.gift.command.sendGift.stringOptionName)}并说: ${gift.giftData.giftAnnouncement}`,
      embeds: [embed]
    })
  }
}

export { sendGift }
