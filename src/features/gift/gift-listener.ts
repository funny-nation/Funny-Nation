import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { addDbCoinTransfer, getDbGuild, getDbMember } from '../../models'
import { createInventory } from '../../models/db-inventory/create-inventory'
import { getLanguage } from '../../language'
import { Gift } from './gift-type'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return
  if (!interaction.guild) return
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

  const member = await getDbMember(interaction.user.id, interaction.guild.id)
  const presetGifts = language.gift.presetGifts
  type PresetGiftKey = keyof typeof presetGifts
  const gift: Gift | undefined = presetGifts[giftID as PresetGiftKey]
  if (!gift) return
  if (member.coinBalanceInGuild < gift.price) {
    await interaction.reply(language.gift.hasEnoughMoney)
    return
  }
  await member.reduceCoins(gift.price)
  await addDbCoinTransfer(member.userID, interaction.guild.id, gift.price, null, '', 'sendGift')
  await createInventory(gift.name, 'gift', interaction.user.id, receiver.id)

  await interaction.reply(gift.announcement(interaction.user, receiver))

  const receverDM = await receiver.createDM()

  const embed = new MessageEmbed()
    .setTitle(language.gift.embedTitle)
    .setDescription(language.gift.embedDesc)
    .setColor('#FF99CC')
  await receverDM.send({
    embeds: [embed]
  })
})
