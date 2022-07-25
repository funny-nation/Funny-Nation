import { REST } from '@discordjs/rest'
import { Routes } from 'discord-api-types/v9'
import discordToken from '../discord-token'
import client from '../client'
import logger from '../logger'
import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import { DBGuild } from '../models/DBGuild'

/**
 * HTTP request to Discord api for setting up commands for a specific discord
 * @param commands
 * @param guild
 */
async function commandSetup (commands: (SlashCommandBuilder | ContextMenuCommandBuilder | any)[], guild: DBGuild) {
  if (client.user === null) {
    logger.error('Cannot setup commands because client\'s user does not existed')
    process.exit(2)
  }
  const commandRequestBody = []
  for (const command of commands) {
    commandRequestBody.push(command.toJSON())
  }
  const rest = new REST({ version: '9' }).setToken(discordToken)
  const discordGuilds = await client.guilds.fetch(guild.id)
  await rest.put(Routes.applicationGuildCommands(client.user.id, guild.id), { body: commandRequestBody })
  logger.info(`All commands for guild ${discordGuilds.name} have been set`)
}

export default commandSetup
