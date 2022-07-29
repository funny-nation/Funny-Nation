import {
  MessageEmbed,
  ModalSubmitInteraction
} from 'discord.js'
import { client } from '../../../client'
import { getDbGuild } from '../../../models'
import { getNotificationChannelByGuild } from '../../../utils'
import { logger } from '../../../logger'
import { getLanguage } from '../../../language'

const notificationSendHandler = async (interaction: ModalSubmitInteraction) => {
  const guilds = await client.guilds.fetch()
  const notificationMsg = interaction.fields.getTextInputValue('input')
  const targetLanguage = interaction.fields.getTextInputValue('language')
  const nameOfGuildsReceived = []
  const nameOfGuildsSentFailed = []
  let numOfGuildUseThisInLanguage = 0
  for (const [guildID, guild] of guilds) {
    const dbGuild = await getDbGuild(guildID)
    if (dbGuild.languageInGuild !== targetLanguage) continue
    numOfGuildUseThisInLanguage += 1
    const discordGuild = await guild.fetch()
    const notificationChannel = await getNotificationChannelByGuild(discordGuild)
    let sent = false
    if (notificationChannel) {
      try {
        const lan = getLanguage(targetLanguage)
        await notificationChannel.send({
          embeds: [
            new MessageEmbed()
              .setTitle(lan.notification)
              .setColor('#FF99CC')
              .setDescription(notificationMsg)
          ]
        })
        logger.verbose(`Notification has been sent to channel "${notificationChannel.name}"`)
        sent = true
      } catch (e) {
        sent = false
      }
    }
    if (sent) {
      nameOfGuildsReceived.push(discordGuild.name)
    } else {
      nameOfGuildsSentFailed.push(discordGuild.name)
    }
  }

  let nameOfGuildsReceivedString = '\n'
  let nameOfGuildsRejectString = '\n'

  for (const name of nameOfGuildsReceived) {
    nameOfGuildsReceivedString += `- ${name} \n`
  }
  for (const name of nameOfGuildsSentFailed) {
    nameOfGuildsRejectString += `- ${name} \n`
  }

  const statResult = `There are ${numOfGuildUseThisInLanguage} guilds using this bot with this language. \n**Guilds that received: **${nameOfGuildsReceivedString}**Guilds that failed: **${nameOfGuildsRejectString}`
  await interaction.reply(statResult)
}

export { notificationSendHandler }
