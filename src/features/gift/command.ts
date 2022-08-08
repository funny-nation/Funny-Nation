import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { Gift } from './gift-type'

newCommand(
  language => new SlashCommandBuilder()
    .setName(language.gift.command.name)
    .setDescription(language.gift.command.desc)
    .addSubcommand(
      subcommand => subcommand
        .setName(language.gift.command.subCommand.name)
        .setDescription(language.gift.command.subCommand.desc)
        .addStringOption(
          option => {
            const opts = option
              .setName(language.gift.command.subCommand.stringOptionName)
              .setDescription(language.gift.command.subCommand.stringOptionDesc)
              .setRequired(true)
            const presetGifts = language.gift.presetGifts
            type PresetGiftKey = keyof typeof presetGifts
            for (const giftKey in presetGifts) {
              const gift: Gift = presetGifts[giftKey as PresetGiftKey]
              opts.addChoices({
                name: gift.name,
                value: giftKey
              })
            }
            return opts
          }
        )
        .addUserOption(
          option => option
            .setName(language.gift.command.subCommand.userOptionName)
            .setDescription(language.gift.command.subCommand.userOptionDesc)
            .setRequired(true)
        )
    )
)
