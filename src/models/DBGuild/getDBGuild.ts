import { DBGuild } from './DBGuild'
import prismaClient from '../../prismaClient'
import logger from '../../logger'
import { Guild } from 'discord.js'
import client from '../../client'
import moment from 'moment-timezone'

const getDBGuild = async function (guildID: string): Promise<DBGuild> {
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
        languageUpdatedAt: moment().utc().toDate()
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
          languageUpdatedAt: moment().utc().toDate()
        }
      })
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
    }
  }
}

export default getDBGuild
