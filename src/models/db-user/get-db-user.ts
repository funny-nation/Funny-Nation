import { DBUser } from './db-user'
import { prismaClient } from '../../prisma-client'
import moment from 'moment-timezone'
import { logger } from '../../logger'
import { User } from 'discord.js'
import { client } from '../../client'

const getDbUser = async function (userID: string): Promise<DBUser> {
  let userInDB = await prismaClient.user.findUnique({
    where: {
      id: userID
    }
  })

  if (userInDB === null) {
    userInDB = await prismaClient.user.create({
      data: {
        id: userID,
        experience: 0,
        timeBefore: moment().utc().toDate()
      }
    })
    const discordUser: User = await client.users.fetch(userID)
    logger.info(`New User ${discordUser.tag} has been created`)
  }
  const dbUser: DBUser = {
    ...userInDB,
    async resetTimeBefore () {
      const now = moment().utc().toDate()
      await prismaClient.user.update({
        where: {
          id: userID
        },
        data: {
          timeBefore: now
        }
      })
      this.timeBefore = now
    },
    async addExperience (exp: number = 1) {
      const updatedUser = await prismaClient.user.update({
        where: {
          id: userID
        },
        data: {
          experience: {
            increment: exp
          }
        }
      })
      this.experience = updatedUser.experience
    },
    async setAnonymousNickName (anonymousNickName:string) {
      await prismaClient.user.update({
        where: {
          id: userID
        },
        data: {
          anonymousNickName
        }
      })
      this.anonymousNickName = anonymousNickName
    },
    async getExpRanking () {
      const aggResult = await prismaClient.user.aggregate({
        where: {
          experience: {
            gt: this.experience
          }
        },
        _count: true
      })
      return aggResult._count + 1
    }
  }
  return dbUser
}

export { getDbUser }
