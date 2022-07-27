import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

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
