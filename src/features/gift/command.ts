import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { giftInfo } from './gift-info'

newCommand(
  language => new SlashCommandBuilder()
    .setName('gift')
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
            for (const [giftKey, gift] of giftInfo) {
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
