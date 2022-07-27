import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand((language: Language) => new SlashCommandBuilder()
  .setName(language.commands.getMyProfile.name)
  .setDescription(language.commands.getMyProfile.desc)
)
