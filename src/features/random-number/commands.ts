import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  () => new SlashCommandBuilder()
    .setName('random-number')
    .setDescription('为您生成对应设置的随机数')
    .addSubcommand(
      subcommand => subcommand
        .setName('随机数')
        .setDescription('随机数111123')
        .addIntegerOption(option => option
          .setName('第一个数')
          .setRequired(true)
          .setDescription('生成范围')
        )
        .addIntegerOption(option => option
          .setName('第二个数')
          .setRequired(true)
          .setDescription('生成范围')
        )
        .addIntegerOption(option => option
          .setName('生成个数')
          .setRequired(true)
          .setDescription('生成个数')
          .setMinValue(1)
        )
    )
)
