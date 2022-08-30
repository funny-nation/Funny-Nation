import { GuildMember } from 'discord.js'
import { getDbGuild } from '../models'

/**
 * Check if a member is an administrator of that guild or not.
 * @param member
 */
const isAdmin = async (member: GuildMember): Promise<boolean> => {
  let hasPermission = member.permissions.has('ADMINISTRATOR')
  hasPermission = hasPermission || (member.guild.ownerId === member.id)
  const dbGuild = await getDbGuild(member.guild.id)
  if (dbGuild.administratorRoleID !== null) {
    hasPermission = hasPermission || member.roles.cache.has(dbGuild.administratorRoleID)
  }
  return hasPermission
}

export { isAdmin }
