import { client } from '../../client'
import { logger } from '../../logger'
import { Message, MessageEmbed } from 'discord.js'
import { getDbUser, DBUser, getDbMember, DBMember, addDbCoinTransfer, getDbGuild } from '../../models'
import moment from 'moment-timezone'
import { getLanguage } from '../../language'

client.on('messageCreate', async function (message: Message) {
  try {
    if (!message.guild) return
    logger.verbose(`${message.author.tag} send "${message.content}"`)
    const user: DBUser = await getDbUser(message.author.id)
    if (!message.member) return

    const member: DBMember = await getDbMember(message.member.id, message.guild.id)
    const userLastPresentTime = user.timeBefore
    const nowTime = moment.utc().toDate()
    const timeDeltaInMS = nowTime.getTime() - userLastPresentTime.getTime()
    if (timeDeltaInMS < 60000) {
      return
    }
    if (userLastPresentTime.getDate() !== nowTime.getDate()) {
      if (message.member.premiumSince) {
        const dbGuild = await getDbGuild(message.guild.id)
        const language = getLanguage(dbGuild.languageInGuild)
        await member.addCoins(60)
        await addDbCoinTransfer(user.id, message.guild.id, 60, null, '', 'earnFromCheckIn')
        logger.verbose(`Booster ${message.author.tag} earns 60 by check in`)
        await message.channel.send({
          content: `${message.author}`,
          embeds: [
            new MessageEmbed()
              .setTitle(language.dailyCheckIn.titleForBooster)
              .setDescription(language.dailyCheckIn.desc(60))
              .setColor('#FF99CC')
          ]
        })
      }
    }
    await user.resetTimeBefore()
    await user.addExperience()
    logger.verbose(`Add 1 exp to user ${message.author.tag}`)
    await member.addCoins()
    logger.verbose(`Add 1 coin to member ${message.author.tag} in guild ${message.guild.name}`)
    await addDbCoinTransfer(message.author.id, message.guild.id, 1, null, '', 'earnFromMessage')
    await member.addMemberExperience()
    logger.verbose(`Add 1 exp to member ${message.author.tag} in guild ${message.guild.name}`)
  } catch (e) {
    console.log(e)
    logger.error('Error on create-and-add-coins-exp')
  }
})
