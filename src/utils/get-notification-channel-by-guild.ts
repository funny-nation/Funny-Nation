import { Guild, NewsChannel, TextChannel, VoiceChannel } from 'discord.js'
import { getDbGuild } from '../models'
import { logger } from '../logger'

/**
 * Get the notification by a guild object from discord.js
 * return null if notification channel does not found
 * @param guild
 * @return a text based channel
 */
const getNotificationChannelByGuild = async (guild: Guild): Promise<NewsChannel | TextChannel | VoiceChannel | null> => {
  const dbGuild = await getDbGuild(guild.id)
  if (dbGuild.notificationChannelID) {
    const channel = await guild.channels.fetch(dbGuild.notificationChannelID)
    if (channel) {
      const targetChannel = await channel.fetch()
      if (targetChannel.isText()) {
        return targetChannel
      }
    }
  }
  logger.verbose(`Does not found text channel by id ${guild.id}, now sending to system channel`)
  if (guild.systemChannel !== null) {
    return guild.systemChannel
  }
  return null
}

export { getNotificationChannelByGuild }
