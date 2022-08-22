import { Badge } from '@prisma/client'
import { prismaClient } from '../../prisma-client'

class DBBadge {
  badgeData: Badge
  private constructor (badge: Badge) {
    this.badgeData = badge
  }

  public static async fetchByID (id: number): Promise<DBBadge | null> {
    const badge = await prismaClient.badge.findUnique({
      where: {
        id
      }
    })
    if (!badge) {
      return null
    }
    return new this(badge)
  }

  public static async fetchByName (name: string): Promise<DBBadge | null> {
    const badge = await prismaClient.badge.findFirst({
      where: {
        name
      }
    })
    if (!badge) {
      return null
    }
    return new this(badge)
  }

  public static async fetchByGuild (guildID: string): Promise<DBBadge[]> {
    const dbBadges: DBBadge[] = []
    const badges = await prismaClient.badge.findMany({
      where: {
        guildID
      }
    })
    for (const badge of badges) {
      dbBadges.push(new this(badge))
    }
    return dbBadges
  }

  public static async create (name: string, emoji: string, desc: string, price: number, roleIDRelated: string, guildID: string): Promise<DBBadge | null> {
    const existedBadge = await this.fetchByName(name)
    if (existedBadge) {
      return null
    }
    const newBadge = await prismaClient.badge.create({
      data: {
        name,
        emoji,
        desc,
        price,
        roleIDRelated,
        guildID
      }
    })
    return new this(newBadge)
  }

  async delete () {
    await prismaClient.badge.delete({
      where: {
        id: this.badgeData.id
      }
    })
  }
}

export { DBBadge }
