import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import getLanguage from '../language/get-language'
import { DBGuild } from '../models/db-guild'
import commandSetup from '../utils/command-setup'
import { ApplicationCommandType } from 'discord-api-types/v10'

async function setCommands (guild: DBGuild) {
  const language = getLanguage(guild.languageInGuild)
  // Put your commands right here in this list
  const commandsList = [
    new SlashCommandBuilder()
      .setName(language.transferCoin.transferCommand)
      .setDescription(language.transferCoin.commandDesc)
      .addSubcommand(
        subcommand => subcommand
          .setName(language.transferCoin.coin)
          .setDescription(language.transferCoin.coinDesc)
          .addUserOption(option => option
            .setName(language.transferCoin.payee)
            .setRequired(true)
            .setDescription(language.transferCoin.payeeDesc)
          )
          .addIntegerOption(option => option
            .setName(language.transferCoin.coin)
            .setRequired(true)
            .setDescription(language.transferCoin.amountDesc)
          )
          .addStringOption(option => option
            .setName(language.transferCoin.detail)
            .setDescription(language.transferCoin.detailDesc)
          )
      ),
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
