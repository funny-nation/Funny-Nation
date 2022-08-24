import { Badge } from '@prisma/client'
import { prismaClient } from '../../prisma-client'

class DBBadge {
  badgeData: Badge
  static badgePrisma = prismaClient.badge
  static memberBadgePrisma = prismaClient.memberBadge

  private constructor (badge: Badge) {
    this.badgeData = badge
  }

  public static async fetchByID (id: number): Promise<DBBadge | null> {
    const badge = await this.badgePrisma.findUnique({
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
    const badge = await this.badgePrisma.findFirst({
      where: {
        name
      }
    })
    if (!badge) {
      return null
    }
    return new this(badge)
  }

  public static async fetchManyByGuild (guildID: string): Promise<DBBadge[]> {
    const dbBadges: DBBadge[] = []
    const badges = await this.badgePrisma.findMany({
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
    const newBadge = await this.badgePrisma.create({
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

  public static async countBadgesInGuild (guildID: string): Promise<number> {
    const aggResult = await this.badgePrisma.aggregate({
      where: {
        guildID
      },
      _count: true
    })
    return aggResult._count
  }

  async delete () {
    await DBBadge.memberBadgePrisma.deleteMany({
      where: {
        badgeID: this.badgeData.id
      }
    })
    await DBBadge.badgePrisma.delete({
      where: {
        id: this.badgeData.id
      }
    })
  }
}

export { DBBadge }
