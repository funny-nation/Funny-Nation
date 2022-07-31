import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { Language } from '../../language'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName(language.anonymousMsg.command.name)
    .setDescription(language.anonymousMsg.command.desc)
)
