import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName(language.transactionsHistory.commandName)
    .setDescription(language.transactionsHistory.commandDesc)
)
