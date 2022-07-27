import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand((language: Language) => new SlashCommandBuilder()
  .setName(language.setGuildProfile.commands.name)
  .setDescription(language.setGuildProfile.commands.desc)
  .addSubcommand(
    subcommand => subcommand
      .setName(language.setGuildProfile.commands.subcommand.setOthers.name)
      .setDescription(language.setGuildProfile.commands.subcommand.setOthers.desc)
  )
  .addSubcommand(
    subcommand => subcommand
      .setName(language.setGuildProfile.commands.subcommand.setAdmin.name)
      .setDescription(language.setGuildProfile.commands.subcommand.setAdmin.desc)
      .addRoleOption(
        option => option
          .setName(language.setGuildProfile.commands.subcommand.setAdmin.optionName)
          .setDescription(language.setGuildProfile.commands.subcommand.setAdmin.optionDesc)
          .setRequired(true)
      )
  )
  .addSubcommand(
    subcommand => subcommand
      .setName(language.setGuildProfile.commands.subcommand.setAnnouncement.name)
      .setDescription(language.setGuildProfile.commands.subcommand.setAnnouncement.desc)
      .addChannelOption(
        option => option
          .setName(language.setGuildProfile.commands.subcommand.setAnnouncement.optionName)
          .setDescription(language.setGuildProfile.commands.subcommand.setAnnouncement.optionDesc)
          .setRequired(true)
      )
  )
  .addSubcommand(
    subcommand => subcommand
      .setName(language.setGuildProfile.commands.subcommand.setNotificationChannel.name)
      .setDescription(language.setGuildProfile.commands.subcommand.setNotificationChannel.desc)
      .addChannelOption(
        option => option
          .setName(language.setGuildProfile.commands.subcommand.setNotificationChannel.optionName)
          .setDescription(language.setGuildProfile.commands.subcommand.setNotificationChannel.optionDesc)
          .setRequired(true)
      )
  )
)
