import { DBMember } from './db-member'
import { prismaClient } from '../../prisma-client'
import { logger } from '../../logger'
import { client } from '../../client'
import { Guild, User } from 'discord.js'
import { getDbUser } from '../db-user'

const getDbMember = async function (userID: string, guildID: string): Promise<DBMember> {
  let memberInDB = await prismaClient.member.findUnique({
    where: {
      userID_guildID: {
        userID,
        guildID
      }
    }
  })
  if (memberInDB === null) {
    await getDbUser(userID)
    memberInDB = await prismaClient.member.create({
      data: {
        userID,
        guildID,
        experienceInGuild: 0,
        coinBalanceInGuild: 0
      }
    })
    const discordUser: User = await client.users.fetch(userID)
    const guild: Guild = await client.guilds.fetch(guildID)
    logger.info(`New member ${discordUser.tag} has been created associate with guild ${guild.name}`)
  }
  const dbMember: DBMember = {
    ...memberInDB,
    async addMemberExperience (exp: number = 1): Promise<void> {
      const newMember = await prismaClient.member.update({
        where: {
          userID_guildID: {
            userID,
            guildID
          }
        },
        data: {
          experienceInGuild: {
            increment: exp
          }
        }
      })
      this.experienceInGuild = newMember.experienceInGuild
    },
    async addCoins (coins: number = 1): Promise<void> {
      const newMember = await prismaClient.member.update({
        where: {
          userID_guildID: {
            userID,
            guildID
          }
        },
        data: {
          coinBalanceInGuild: {
            increment: coins
          }
        }
      })
      this.coinBalanceInGuild = newMember.coinBalanceInGuild
    },
    async reduceCoins (coins: number = 1) {
      const newMember = await prismaClient.member.update({
        where: {
          userID_guildID: {
            userID,
            guildID
          }
        },
        data: {
          coinBalanceInGuild: {
            decrement: coins
          }
        }
      })
      this.coinBalanceInGuild = newMember.coinBalanceInGuild
    },
    async getExpRanking () {
      const aggResult = await prismaClient.member.aggregate({
        where: {
          guildID,
          experienceInGuild: {
            gt: this.experienceInGuild
          }
        },
        _count: true
      })
      return aggResult._count + 1
    },
    async getCoinRanking () {
      const aggResult = await prismaClient.member.aggregate({
        where: {
          guildID,
          coinBalanceInGuild: {
            gt: this.coinBalanceInGuild
          }
        },
        _count: true
      })
      return aggResult._count + 1
    }
  }
  return dbMember
}

export { getDbMember }
