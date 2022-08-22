import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { addDbCoinTransfer, getDbGuild, getDbMember } from '../../models'
// import { createInventory } from '../../models/db-inventory/create-inventory'
import { getLanguage } from '../../language'
import { Gift } from './gift-type'
import { expAdjustment } from './exp-adjustment'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand() || !interaction.guild) return
    // localization
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = await getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.gift.command.name) return
    const giftID = interaction.options.getString(language.gift.command.subCommand.stringOptionName)
    const receiver = interaction.options.getUser(language.gift.command.subCommand.userOptionName)

    if (!giftID || !receiver) return

    if (!client.user) return
    if (receiver.id === client.user.id) {
      await interaction.reply(language.gift.errorHandler.botReply)
      return
    }
    if (receiver.id === interaction.user.id) {
      await interaction.reply(language.gift.errorHandler.userReply)
      return
    }
    // query sender and receiver from db with ids
    const senderInfo = await getDbMember(interaction.user.id, interaction.guild.id)
    const receiverInfo = await getDbMember(receiver.id, interaction.guild.id)
    const presetGifts = language.gift.presetGifts
    type PresetGiftKey = keyof typeof presetGifts
    const gift: Gift | undefined = presetGifts[giftID as PresetGiftKey]
    if (!gift) return
    if (senderInfo.coinBalanceInGuild < gift.price) {
      await interaction.reply(language.gift.hasEnoughMoney)
      return
    }
    // adjust money and exp between gift sender and receiver after gift sent
    const price = gift.price
    await senderInfo.reduceCoins(price)
    await senderInfo.addMemberExperience(expAdjustment(price).senderExp)
    await receiverInfo.addMemberExperience(expAdjustment(price).receiverExp)
    await addDbCoinTransfer(senderInfo.userID, interaction.guild.id, gift.price, null, '', 'sendGift')
    // await createInventory(gift.name, 'gift', interaction.user.id, receiver.id, interaction.guild.id)

    await interaction.reply({
      content: gift.announcement(interaction.user, receiver),
      embeds: [
        new MessageEmbed()
          .setTitle(gift.name)
          .setDescription(gift.desc)
          .setColor('#FF99CC')
          .setThumbnail(gift.pictureURL)
      ]
    })

    const receverDM = await receiver.createDM()

    const embed = new MessageEmbed()
      .setTitle(language.gift.embedTitle)
      .setDescription(language.gift.embedDesc)
      .setColor('#FF99CC')
    await receverDM.send({
      embeds: [embed]
    })
  } catch (e) {
    console.log(e)
    logger.error('error occurs when executing features/gift/gift-listener')
  }
})
