import { DBGuild } from './DBGuild'
import prismaClient from '../../prismaClient'
import logger from '../../logger'
import { Guild } from 'discord.js'
import client from '../../client'

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
        timeZone: 'America/New_York'
      }
    })
    const guild: Guild = await client.guilds.fetch(guildID)
    logger.info(`New Guild ${guild.name} has been created`)
  }
  return dbGuild
}

export default getDBGuild
