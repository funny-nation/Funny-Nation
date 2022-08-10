import { newCommand } from '../../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  () => new SlashCommandBuilder()
    .setName('dealer')
    .setDescription('dealer for tabletop.ts game')
    .addSubcommand(
      subcommand => subcommand
        .setName('custom-single')
        .setDescription('Dealers with customizable card contents and number of players, one card per player')
    )
)
