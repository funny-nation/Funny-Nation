import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'
import { newCommand } from '../../commands-manager'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName(language.monetaryControl.coinCommand)
    .setDescription(language.monetaryControl.coinDesc)
    .addSubcommand(subcommand => subcommand
      .setName(language.monetaryControl.issueSubcommand)
      .setDescription(language.monetaryControl.issueDesc)
      .addIntegerOption(option => option
        .setName(language.monetaryControl.amountOption)
        .setDescription(language.monetaryControl.amountDesc)
        .setRequired(true)
        .setMinValue(1)
      )
      .addUserOption(option => option
        .setName(language.monetaryControl.targetUserOption)
        .setDescription(language.monetaryControl.targetUserDesc)
        .setRequired(true)
      )
    )
    .addSubcommand(subcommand => subcommand
      .setName(language.monetaryControl.collectSubcommand)
      .setDescription(language.monetaryControl.collectDesc)
      .addIntegerOption(option => option
        .setName(language.monetaryControl.amountOption)
        .setDescription(language.monetaryControl.amountDesc)
        .setRequired(true)
        .setMinValue(1)
      )
      .addUserOption(option => option
        .setName(language.monetaryControl.targetUserOption)
        .setDescription(language.monetaryControl.targetUserDesc)
        .setRequired(true)
      )
    )
)
