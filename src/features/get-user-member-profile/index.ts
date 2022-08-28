import { client } from '../../client'
import {
  Interaction,
  MessageEmbed
} from 'discord.js'
import { getLanguage } from '../../language'
import { DBGuild, getDbGuild, DBUser, getDbUser, DBMember, getDbMember } from '../../models'
import { renderExpBar } from './render-exp-bar'
import { calculateLevelByExp } from '../../utils'
import { logger } from '../../logger'
import './commands'
import { DBMemberBadge } from '../../models/db-badge'

client.on('interactionCreate', async function (interaction: Interaction) {
  try {
    if (!interaction.isCommand()) return
    if (interaction.guild === null || interaction.member === null) return
    const dbUser: DBUser = await getDbUser(interaction.user.id)
    const dbMember: DBMember = await getDbMember(interaction.user.id, interaction.guild.id)
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.commands.getMyProfile.name) return
    const coinRanking = await dbMember.getCoinRanking()
    const expInGuildRanking = await dbMember.getExpRanking()
    const expInBotRanking = await dbUser.getExpRanking()
    const memberBadges = await DBMemberBadge.fetchBadgesByMember(dbUser.id, dbGuild.id)
    let badgeEmojiStr = ''
    for (const memberBadge of memberBadges) {
      const dbBadge = await memberBadge.getDBBadge()
      if (!dbBadge) continue
      badgeEmojiStr += dbBadge.badgeData.emoji + ' • '
    }
    const embedMsg = new MessageEmbed()
      .setColor('#FF99CC')
      .setDescription(badgeEmojiStr)
      .setTitle(language.coinBalanceDisplay(Number(dbMember.coinBalanceInGuild), coinRanking))
      .setAuthor({ name: language.viewProfile.profile })
      .addFields(
        {
          name: `Level ${Math.floor(calculateLevelByExp(Number(dbMember.experienceInGuild)))}        ${renderExpBar(Number(dbMember.experienceInGuild))}`,
          value: language.viewProfile.expInThisGuild(interaction.guild.name, expInGuildRanking) + '\n.',
          inline: false
        },
        {
          name: `Level ${Math.floor(calculateLevelByExp(Number(dbUser.experience)))}        ${renderExpBar(Number(dbUser.experience))}`,
          value: language.viewProfile.expInThisBot(expInBotRanking),
          inline: false
        }
      )
    const avatarUrl = interaction.user.avatarURL()
    if (avatarUrl !== null) {
      embedMsg.setThumbnail(avatarUrl)
      embedMsg.setAuthor({ name: interaction.user.tag, iconURL: avatarUrl })
    }
    await interaction.reply({ embeds: [embedMsg] })
  } catch (e) {
    console.log(e)
    logger.error(`Error when ${interaction.user.tag} try to get his profile`)
  }
})
