import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  (language) => new SlashCommandBuilder()
    .setName('random-number')
    .setDescription('为您生成对应设置的随机数')
    .addSubcommand(
      subcommand => subcommand
        .setName(language.randomNumber.subcommandName)
        .setDescription(language.randomNumber.subcommandDescription)
        .addIntegerOption(option => option
          .setName(language.randomNumber.firstNumberOptionName)
          .setRequired(true)
          .setDescription(language.randomNumber.firstNumberOptionDescription)
        )
        .addIntegerOption(option => option
          .setName(language.randomNumber.secondNumberOptionName)
          .setRequired(true)
          .setDescription(language.randomNumber.secondNumberOptionDescription)
        )
        .addIntegerOption(option => option
          .setName(language.randomNumber.rangeNumberOptionName)
          .setRequired(true)
          .setDescription(language.randomNumber.rangeNumberOptionDescription)
          .setMinValue(1)
        )
    )
)
