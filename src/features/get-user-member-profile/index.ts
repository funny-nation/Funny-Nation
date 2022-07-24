import client from '../../client'
import {
  Interaction,
  MessageEmbed
} from 'discord.js'
import getLanguage from '../../language/getLanguage'
import { DBGuild } from '../../models/DBGuild'
import getDBGuild from '../../models/DBGuild/getDBGuild'
import { DBUser } from '../../models/DBUser'
import getDBUser from '../../models/DBUser/getDBUser'
import { DBMember } from '../../models/DBMember'
import getDBMember from '../../models/DBMember/getDBMember'
import renderExpBar from './render-exp-bar'
import calculateLevelByExp from './calculate-level-by-exp'
import logger from '../../logger'

client.on('interactionCreate', async function (interaction: Interaction) {
  if (!interaction.isCommand()) return
  if (interaction.guild === null || interaction.member === null) return
  try {
    const dbUser: DBUser = await getDBUser(interaction.user.id)
    const dbMember: DBMember = await getDBMember(interaction.user.id, interaction.guild.id)
    const dbGuild: DBGuild = await getDBGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.commands.getMyProfile.name) return
    const embedMsg = new MessageEmbed()
      .setColor('#FF99CC')
      .setTitle(language.coinBalanceDisplay(Number(dbMember.coinBalanceInGuild)))
      .setAuthor({ name: language.viewProfile.profile })
      .addFields(
        {
          name: `Level ${Math.floor(calculateLevelByExp(Number(dbMember.experienceInGuild)))}        ${renderExpBar(Number(dbMember.experienceInGuild))}`, value: language.viewProfile.inXXX(interaction.guild.name) + '\n.', inline: false
        },
        {
          name: `Level ${Math.floor(calculateLevelByExp(Number(dbUser.experience)))}        ${renderExpBar(Number(dbMember.experienceInGuild))}`, value: language.viewProfile.yourExp, inline: false
        }
      )
    const avatarUrl = interaction.user.avatarURL()
    if (avatarUrl !== null) {
      embedMsg.setThumbnail(avatarUrl)
      embedMsg.setAuthor({ name: interaction.user.tag, iconURL: avatarUrl })
    }
    await interaction.reply({ embeds: [embedMsg] })
  } catch (e) {
    await interaction.reply('Error')
    console.log(e)
    logger.error(`Error when ${interaction.user.tag} try to get his profile`)
  }
})
