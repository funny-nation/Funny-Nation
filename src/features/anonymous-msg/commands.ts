import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { Language } from '../../language'

newCommand(
  (language: Language) => new SlashCommandBuilder()
    .setName('anonymous')
    .setDescription(language.anonymousMsg.commands.desc)
    .addSubcommand(
      subcommand => subcommand
        .setName(language.anonymousMsg.commands.setName.name)
        .setDescription(language.anonymousMsg.commands.setName.desc)
        .addStringOption(
          option => option
            .setName(language.anonymousMsg.commands.setName.optionName)
            .setDescription(language.anonymousMsg.commands.setName.optionName)
            .setMaxLength(20)
            .setRequired(true)
        )
    )
    .addSubcommand(
      subcommand => subcommand
        .setName(language.anonymousMsg.commands.send.name)
        .setDescription(language.anonymousMsg.commands.send.desc)
        .addStringOption(
          option => option
            .setName(language.anonymousMsg.commands.send.MsgOptionName)
            .setDescription(language.anonymousMsg.commands.send.MsgOptionName)
            .setRequired(true)
        )
        .addUserOption(
          option => option
            .setName(language.anonymousMsg.commands.send.UserOptionName)
            .setDescription(language.anonymousMsg.commands.send.UserOptionName)
            .setRequired(false)
        )
    )
)
