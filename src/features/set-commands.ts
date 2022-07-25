import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import getLanguage from '../language/getLanguage'
import { DBGuild } from '../models/DBGuild'
import commandSetup from '../utils/commandSetup'
import { ApplicationCommandType } from 'discord-api-types/v10'

async function setCommands (guild: DBGuild) {
  const language = getLanguage(guild.languageInGuild)
  // Put your commands right here in this list
  const commandsList = [
    new SlashCommandBuilder()
      .setName(language.commands.getMyProfile.name)
      .setDescription(language.commands.getMyProfile.desc),
    new ContextMenuCommandBuilder()
      .setName(language.mumble.mumble)
      .setType(ApplicationCommandType.User),
    new SlashCommandBuilder()
      .setName(language.setGuildProfile.command)
      .setDescription(language.setGuildProfile.commandDesc)
      .addSubcommand(
        subcommand => subcommand
          .setName('lt')
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
          .addRoleOption(
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
          .addRoleOption(
            option => option
              .setName('channel')
              .setDescription('Notification Channel')
              .setRequired(true)
          )
      )
  ]
  await commandSetup(commandsList, guild)
}

export default setCommands
