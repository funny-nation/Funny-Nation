import { DBMember } from './db-member'
import { prismaClient } from '../../prisma-client'
import { logger } from '../../logger'
import { client } from '../../client'
import { Guild, User } from 'discord.js'
import { getDbUser } from '../db-user'

const getDbMember = async function (userID: string, guildID: string): Promise<DBMember> {
  let dbMember = await prismaClient.member.findUnique({
    where: {
      userID_guildID: {
        userID,
        guildID
      }
    }
  })
  if (dbMember === null) {
    await getDbUser(userID)
    dbMember = await prismaClient.member.create({
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
  return {
    ...dbMember,
    async addMemberExperience (exp: number = 1): Promise<void> {
      await prismaClient.member.update({
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
      super.experienceInGuild += exp
    },
    async addCoins (coins: number = 1): Promise<void> {
      await prismaClient.member.update({
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
      super.coinBalanceInGuild += coins
    },
    async reduceCoins (coins: number = 1) {
      await prismaClient.member.update({
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
      super.coinBalanceInGuild -= coins
    }
  }
}

export { getDbMember }
