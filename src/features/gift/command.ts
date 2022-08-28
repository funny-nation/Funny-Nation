import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'
import { DBGift } from '../../models/db-gift/creat-gift'

newCommand(
  async (language: Language, guildID: string) => {
    const giftList = await DBGift.getGiftList(guildID)
    return new SlashCommandBuilder()
      .setName(language.gift.command.name)
      .setDescription((language.gift.command.desc))
      .addSubcommand(
        subcommand => subcommand
          .setName(language.gift.command.sendGift.name)
          .setDescription(language.gift.command.sendGift.desc)
          .addStringOption(option => {
            const opts = option
              .setName(language.gift.command.sendGift.stringOptionName)
              .setDescription(language.gift.command.sendGift.stringOptionDesc)
              .setMaxLength(20)
              .setRequired(true)
            giftList.forEach((gift) => {
              opts.addChoices({
                name: gift.giftData.name,
                value: gift.giftData.name
              })
            })
            return opts
          }
          )
          .addUserOption(option => option
            .setName(language.gift.command.sendGift.userOptionName)
            .setDescription(language.gift.command.sendGift.userOptionDesc)
            .setRequired(true)
          )
      )
      .addSubcommand(
        subcommand => subcommand
          .setName(language.gift.command.createGift.name)
          .setDescription(language.gift.command.createGift.desc)
          .addStringOption(option => option
            .setName(language.gift.command.createGift.stringOptionName)
            .setDescription(language.gift.command.createGift.stringOptionDesc)
            .setMaxLength(20)
            .setRequired(true)
          )
          .addStringOption(option => option
            .setName(language.gift.command.createGift.emojiOptionName)
            .setMaxLength(20)
            .setDescription(language.gift.command.createGift.emojiOptionDesc)
            .setRequired(true)
          )
          .addNumberOption(option => option
            .setName(language.gift.command.createGift.numberOptionName)
            .setMinValue(1)
            .setDescription(language.gift.command.createGift.numberOptionDesc)
            .setRequired(true)
          )
      )
      .addSubcommand(
        subcommand => subcommand
          .setName(language.gift.command.removeGift.name)
          .setDescription(language.gift.command.removeGift.desc)
          .addStringOption(option => {
            const opts2 = option
              .setName(language.gift.command.removeGift.stringOptionName)
              .setDescription(language.gift.command.removeGift.stringOptionDesc)
              .setMaxLength(20)
              .setRequired(true)
            giftList.forEach((gift) => {
              opts2.addChoices({
                name: gift.giftData.name,
                value: gift.giftData.name
              })
            })
            return opts2
          }
          )
      )
  }
)
