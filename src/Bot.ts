import client from './client'
import discordToken from './discord-token'
import logger from './logger'
import isTest from './isTest'

client.login(discordToken).catch((reason: string) => {
  logger.error('Bot start failed')
  logger.error(reason)
})

client.on('ready', async () => {
  if (client.user === null) {
    return
  }
  logger.info(`Bot logged in as "${client.user.username}" with ID ${client.user.id}`)
  if (isTest()) {
    logger.info('Test passed, now the process is going to be closed')
    process.exit(0)
  }
})
