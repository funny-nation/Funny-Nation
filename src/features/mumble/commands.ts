import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { ContextMenuCommandBuilder } from '@discordjs/builders'
import { ApplicationCommandType } from 'discord-api-types/v10'

newCommand(
  (language: Language) => new ContextMenuCommandBuilder()
    .setName(language.mumble.mumble)
    .setType(ApplicationCommandType.User)
)
