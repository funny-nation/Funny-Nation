import { client } from './client'
import { discordToken } from './discord-token'
import { logger } from './logger'
import { isTest } from './utils'

let botStarted = false

const isBotStarted = () => {
  return botStarted
}

client.login(discordToken).catch((reason: string) => {
  logger.error('Bot start failed')
  logger.error(reason)
})

client.on('ready', async () => {
  botStarted = true
  if (client.user === null) return
  logger.info(`Bot logged in as ${client.user.tag}`)
  if (isTest()) {
    logger.info('Test passed, now the process is going to be closed')
    process.exit(0)
  }
})

export { isBotStarted }
