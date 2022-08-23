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
          .setName(language.gift.command.subCommand.name)
          .setDescription(language.gift.command.subCommand.desc)
          .addStringOption(option => {
            const opts = option
              .setName(language.gift.command.subCommand.stringOptionName)
              .setDescription(language.gift.command.subCommand.stringOptionDesc)
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
            .setName(language.gift.command.subCommand.userOptionName)
            .setDescription(language.gift.command.subCommand.userOptionDesc)
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
            .setName(language.gift.command.createGift.emojiOptionDesc)
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
  }
)
