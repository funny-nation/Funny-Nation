import { DBGuild } from './db-guild'
import { prismaClient } from '../../prisma-client'
import { logger } from '../../logger'
import { Guild } from 'discord.js'
import { client } from '../../client'
import moment from 'moment-timezone'

const getDbGuild = async function (guildID: string): Promise<DBGuild> {
  let dbGuild = await prismaClient.guild.findUnique({
    where: {
      id: guildID
    }
  })
  if (dbGuild === null) {
    dbGuild = await prismaClient.guild.create({
      data: {
        id: guildID,
        languageInGuild: 'English',
        timeZone: 'America/New_York',
        commandsUpdatedAt: moment().utc().toDate()
      }
    })
    const guild: Guild = await client.guilds.fetch(guildID)
    logger.info(`New Guild ${guild.name} has been created`)
  }
  return {
    ...dbGuild,
    async setLanguageInGuild (languageInGuild): Promise<void> {
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          languageInGuild,
          commandsUpdatedAt: moment().utc().toDate()
        }
      })
      super.languageInGuild = languageInGuild
    },
    async setAdministratorRoleID (administratorRoleID: string): Promise<void> {
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          administratorRoleID
        }
      })
      super.administratorRoleID = administratorRoleID
    },
    async setTimeZone (timeZone: string): Promise<void> {
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          timeZone
        }
      })
      super.timeZone = timeZone
    },
    async setNotificationChannelID (notificationChannelID:string): Promise<void> {
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          notificationChannelID
        }
      })
      super.notificationChannelID = notificationChannelID
    },
    async setAnnouncementChannelID (announcementChannelID): Promise<void> {
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          announcementChannelID
        }
      })
      super.announcementChannelID = announcementChannelID
    },
    async resetCommandsUpdatedAt () {
      const now = moment().utc().toDate()
      await prismaClient.guild.update({
        where: {
          id: guildID
        },
        data: {
          commandsUpdatedAt: now
        }
      })
      super.commandsUpdatedAt = now
    }
  }
}

export { getDbGuild }
