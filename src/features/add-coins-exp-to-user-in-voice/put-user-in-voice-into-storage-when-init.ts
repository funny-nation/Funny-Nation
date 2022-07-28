import { client } from '../../client'
import { Guild } from 'discord.js'
import { attachUserToUIVStorage } from './users-in-voice-storage'
import { logger } from '../../logger'

client.on('ready', async () => {
  const guilds = client.guilds.cache
  for (const [, guild] of guilds) {
    const discordGuild: Guild = await guild.fetch()
    const voiceStates = discordGuild.voiceStates.cache
    for (const [userID, voiceState] of voiceStates) {
      attachUserToUIVStorage(userID)
      logger.verbose(`Detect User "${voiceState.member?.displayName}" in voice`)
    }
  }
})
