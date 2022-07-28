import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import { ApplicationCommandType } from 'discord-api-types/v9'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName(language.transferCoin.transferCommand)
    .setDescription(language.transferCoin.commandDesc)
    .addSubcommand(
      subcommand => subcommand
        .setName(language.transferCoin.coin)
        .setDescription(language.transferCoin.coinDesc)
        .addUserOption(option => option
          .setName(language.transferCoin.payee)
          .setRequired(true)
          .setDescription(language.transferCoin.payeeDesc)
        )
        .addIntegerOption(option => option
          .setName(language.transferCoin.coin)
          .setRequired(true)
          .setDescription(language.transferCoin.amountDesc)
        )
        .addStringOption(option => option
          .setName(language.transferCoin.detail)
          .setDescription(language.transferCoin.detailDesc)
        )
    )
)

newCommand(language => new ContextMenuCommandBuilder()
  .setName(language.transferCoin.commandLang)
  .setType(ApplicationCommandType.User)
)
