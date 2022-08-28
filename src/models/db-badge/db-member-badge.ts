import { MemberBadge } from '@prisma/client'
import { prismaClient } from '../../prisma-client'
import moment from 'moment-timezone'

class DBMemberBadge {
  data: MemberBadge
  constructor (memberBadge: MemberBadge) {
    this.data = memberBadge
  }

  public static async fetchExpiredBadges (): Promise<DBMemberBadge[]> {
    const now = moment().utc().toDate()
    const allMemberBadge = await prismaClient.memberBadge.findMany({
      where: {
        expiredAt: {
          lt: now
        }
      }
    })
    const result: DBMemberBadge[] = []
    for (const memberBadge of allMemberBadge) {
      result.push(new this(memberBadge))
    }
    return result
  }

  public static async fetchBadge (badgeID: number, userID: string, guildID: string): Promise<DBMemberBadge | null> {
    const memberBadge = await prismaClient.memberBadge.findUnique({
      where: {
        badgeID_userID_guildID: {
          badgeID,
          userID,
          guildID
        }
      }
    })
    if (!memberBadge) return null

    return new this(memberBadge)
  }

  public static async buyBadge (badgeID: number, userID: string, guildID: string, autoRenew: boolean): Promise<DBMemberBadge> {
    const dbBadge = await this.fetchBadge(badgeID, userID, guildID)
    if (dbBadge) {
      await dbBadge.extend()
      return dbBadge
    }
    const expiredAt = moment().utc().toDate()
    expiredAt.setDate(expiredAt.getDate() + 30)
    const badgeFromDB = await prismaClient.memberBadge.create({
      data: {
        badgeID,
        userID,
        guildID,
        expiredAt,
        autoRenew
      }
    })
    return new this(badgeFromDB)
  }

  async extend (days = 30) {
    const previousExpireAt = this.data.expiredAt
    let newExpireAt: Date
    const now = moment().utc().toDate()
    if (previousExpireAt.getTime() > now.getTime()) {
      newExpireAt = new Date(previousExpireAt)
      newExpireAt.setDate(newExpireAt.getDate() + days)
    } else {
      newExpireAt = new Date(now)
      newExpireAt.setDate(newExpireAt.getDate() + days)
    }
    await prismaClient.memberBadge.update({
      where: {
        badgeID_userID_guildID: {
          badgeID: this.data.badgeID,
          userID: this.data.userID,
          guildID: this.data.guildID
        }
      },
      data: {
        expiredAt: newExpireAt
      }
    })
    this.data.expiredAt = newExpireAt
  }

  async remove (): Promise<void> {
    await prismaClient.memberBadge.delete({
      where: {
        badgeID_userID_guildID: {
          badgeID: this.data.badgeID,
          userID: this.data.userID,
          guildID: this.data.guildID
        }
      }
    })
  }
}

export { DBMemberBadge }
