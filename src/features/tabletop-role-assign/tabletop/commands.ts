import { newCommand } from '../../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  (language) => new SlashCommandBuilder()
    .setName('role-assign')
    .setDescription(language.tabletopRoleAssign.commandsDescription)
    .addSubcommand(
      subcommand => subcommand
        .setName(language.tabletopRoleAssign.subcommandName)
        .setDescription(language.tabletopRoleAssign.subcommandDescription)
    )
)
