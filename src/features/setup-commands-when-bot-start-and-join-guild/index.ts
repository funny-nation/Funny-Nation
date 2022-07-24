import { Guild } from 'discord.js'
import getDBGuild from '../../models/DBGuild/getDBGuild'
import { DBGuild } from '../../models/DBGuild/DBGuild'
import client from '../../client'
import setCommands from '../commands'
import logger from '../../logger'

client.on('guildCreate', async function (guild: Guild) {
  logger.info(`Bot join guild ${guild.name}`)
  try {
    const dbGuild: DBGuild = await getDBGuild(guild.id)
    await setCommands(dbGuild)
  } catch (e) {
    console.log(e)
    logger.error(`Error when bot set up commands for guild ${guild.name}`)
  }
})

client.on('ready', async function () {
  try {
    const guilds = await client.guilds.fetch()
    for (const [, guild] of guilds) {
      const dbGuild: DBGuild = await getDBGuild(guild.id)
      await setCommands(dbGuild)
      logger.info(`Bot appeared in guild ${guild.name}`)
    }
  } catch (e) {
    console.log(e)
    logger.error('Set up Commands failed when bot is ready')
    process.exit(2)
  }
})
