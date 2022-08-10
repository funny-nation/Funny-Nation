import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  language => new SlashCommandBuilder()
    .setName(language.leaderBoard.command.name)
    .setDescription(language.leaderBoard.command.desc)
)
