import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import { getLanguage } from '../language'
import { DBGuild } from '../models'
import { ApplicationCommandType } from 'discord-api-types/v10'
import { client } from '../client'
import { logger } from '../logger'

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
          .setName('language-time')
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
  ]

  const commandRequestBody = []
  for (const command of commandsList) {
    commandRequestBody.push(command.toJSON())
  }
  const discordGuilds = await client.guilds.fetch(guild.id)
  await discordGuilds.commands.set([])
  await discordGuilds.commands.set(commandRequestBody)
  logger.info(`All commands for guild ${discordGuilds.name} have been set`)
}

export default setCommands
