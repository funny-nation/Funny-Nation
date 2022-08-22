import { Guild, GuildMember, Role } from 'discord.js'
import { getDbGuild } from '../models'

/**
 * Return a list of member that are administrators
 * @param guild
 */
const getAdminListFromAGuild = async (guild: Guild): Promise<GuildMember[]> => {
  const dbGuild = await getDbGuild(guild.id)
  const adminList: GuildMember[] = []
  const owner = await guild.fetchOwner()
  adminList.push(owner)
  if (dbGuild.administratorRoleID) {
    let adminRole: Role | null | undefined = guild.roles.cache.get(dbGuild.administratorRoleID)
    if (!adminRole) {
      adminRole = await guild.roles.fetch(dbGuild.administratorRoleID)
    }
    if (adminRole) {
      for (const [, member] of adminRole.members) {
        adminList.push(member)
      }
    }
  }
  return adminList
}

export { getAdminListFromAGuild }
