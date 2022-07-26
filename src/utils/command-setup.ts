import { client } from '../client'
import { logger } from '../logger'
import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import { DBGuild } from '../models'

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
  console.log(commandRequestBody)
  const discordGuilds = await client.guilds.fetch(guild.id)
  await discordGuilds.commands.set(commandRequestBody)
  logger.info(`All commands for guild ${discordGuilds.name} have been set`)
}

export default commandSetup
