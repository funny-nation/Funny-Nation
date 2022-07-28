import { client } from '../../client'
import { logger } from '../../logger'
import { Message } from 'discord.js'
import { getDbUser, DBUser, getDbMember, DBMember } from '../../models'
import moment from 'moment-timezone'

client.on('messageCreate', async function (message: Message) {
  if (message.guild === null) return
  logger.verbose(`${message.author.tag} send "${message.content}"`)
  try {
    const user: DBUser = await getDbUser(message.author.id)
    if (message.member === null) {
      return
    }
    const member: DBMember = await getDbMember(message.member.id, message.guild.id)
    const userLastPresentTime = user.timeBefore
    const nowTime = moment.utc().toDate()
    const timeDeltaInMS = nowTime.getTime() - userLastPresentTime.getTime()
    if (timeDeltaInMS < 60000) {
      return
    }
    await user.resetTimeBefore()
    await user.addExperience()
    logger.verbose(`Add 1 exp to user ${message.author.tag}`)
    await member.addCoins()
    logger.verbose(`Add 1 coin to member ${message.author.tag} in guild ${message.guild.name}`)
    await member.addMemberExperience()
    logger.verbose(`Add 1 exp to member ${message.author.tag} in guild ${message.guild.name}`)
  } catch (e) {
    console.log(e)
    logger.error('Error on create-and-add-coins-exp')
  }
})
