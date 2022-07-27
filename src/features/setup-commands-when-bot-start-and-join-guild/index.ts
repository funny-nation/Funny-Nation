import { Guild } from 'discord.js'
import { DBGuild, getDbGuild } from '../../models'
import { client } from '../../client'
import { logger } from '../../logger'
import { setUpCommandsForGuild } from '../../commands-manager'

client.on('guildCreate', async function (guild: Guild) {
  logger.info(`Bot join guild ${guild.name}`)
  try {
    const dbGuild: DBGuild = await getDbGuild(guild.id)
    await setUpCommandsForGuild(dbGuild.languageInGuild, guild)
  } catch (e) {
    console.log(e)
    logger.error(`Error when bot set up commands for guild "${guild.name}"`)
  }
})

client.on('ready', async function () {
  try {
    const guilds = await client.guilds.fetch()
    for (const [, guild] of guilds) {
      const dbGuild: DBGuild = await getDbGuild(guild.id)
      const discordGuild: Guild = await guild.fetch()
      await setUpCommandsForGuild(dbGuild.languageInGuild, discordGuild)
      logger.info(`Bot appeared in guild "${guild.name}"`)
    }
  } catch (e) {
    console.log(e)
    logger.error('Set up Commands failed when bot is ready')
    process.exit(2)
  }
})
