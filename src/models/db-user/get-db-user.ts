import { DBUser } from './db-user'
import { prismaClient } from '../../prisma-client'
import moment from 'moment-timezone'
import { logger } from '../../logger'
import { User } from 'discord.js'
import { client } from '../../client'

const getDbUser = async function (userID: string): Promise<DBUser> {
  let dbUser = await prismaClient.user.findUnique({
    where: {
      id: userID
    }
  })

  if (dbUser === null) {
    dbUser = await prismaClient.user.create({
      data: {
        id: userID,
        experience: 0,
        timeBefore: moment().utc().toDate()
      }
    })
    const discordUser: User = await client.users.fetch(userID)
    logger.info(`New User ${discordUser.tag} has been created`)
  }
  return {
    ...dbUser,
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
      super.timeBefore = now
    },
    async addExperience (exp: number = 1) {
      await prismaClient.user.update({
        where: {
          id: userID
        },
        data: {
          experience: {
            increment: exp
          }
        }
      })
      super.experience += exp
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
      super.anonymousNickName = anonymousNickName
    }
  }
}

export { getDbUser }
