import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName('retrieveTransactionHistory')
    .setDescription('retrieve the most recent 10 transactions')
)
