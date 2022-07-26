import { logger } from './logger'

if (process.env.DISCORD_TOKEN === undefined) {
  logger.error('Token not found')
  process.exit(2)
}
const discordToken: string = process.env.DISCORD_TOKEN
export { discordToken }
