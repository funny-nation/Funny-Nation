import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand((language: Language) => new SlashCommandBuilder()
  .setName(language.setGuildProfile.command)
  .setDescription(language.setGuildProfile.commandDesc)
  .addSubcommand(
    subcommand => subcommand
      .setName('others')
      .setDescription('Configure Language and TimeZone')
  )
  .addSubcommand(
    subcommand => subcommand
      .setName('admin')
      .setDescription('Configure Administrator Role')
      .addRoleOption(
        option => option
          .setName('role')
          .setDescription('Administrator Role')
          .setRequired(true)
      )
  )
  .addSubcommand(
    subcommand => subcommand
      .setName('announcement')
      .setDescription('Configure Announcement Channel')
      .addChannelOption(
        option => option
          .setName('channel')
          .setDescription('Announcement Channel')
          .setRequired(true)
      )
  )
  .addSubcommand(
    subcommand => subcommand
      .setName('notification')
      .setDescription('Configure Notification Channel')
      .addChannelOption(
        option => option
          .setName('channel')
          .setDescription('Notification Channel')
          .setRequired(true)
      )
  )
)
