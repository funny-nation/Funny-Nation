import { Guild, GuildMember } from 'discord.js'

const getMemberFromGuild = async (guild: Guild, userID: string): Promise<GuildMember | null> => {
  let member: GuildMember | void = guild.members.cache.get(userID)
  if (!member) {
    member = await guild.members.fetch(userID).catch(() => {
    })
  }
  return member || null
}

export { getMemberFromGuild }
