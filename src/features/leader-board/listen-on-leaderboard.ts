import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { getDbGuild, getLeaderBoard } from '../../models'
import { calculateLevelByExp, getMemberFromGuild } from '../../utils'
import { logger } from '../../logger'
import { getLanguage } from '../../language'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand()) return

    if (!interaction.guild) return

    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = await getLanguage(dbGuild.languageInGuild)
    if (interaction.commandName !== language.leaderBoard.command.name) return

    const leaderboard = await getLeaderBoard(interaction.guild.id)

    const coinsEmbed = new MessageEmbed()
      .setTitle(language.leaderBoard.coinsLeaderBoard)
      .setColor('#FF99CC')
    let number = 1
    for (const memberFromDb of leaderboard.coins) {
      const member = await interaction.guild.members.fetch(memberFromDb.userID)
      coinsEmbed.addFields([{
        name: `#${number} - ${member ? member.displayName : '>_-'}`,
        value: language.leaderBoard.coinsDisplay(Number(memberFromDb.coinBalanceInGuild)),
        inline: true
      }])
      number++
    }

    const expEmbed = new MessageEmbed()
      .setTitle(language.leaderBoard.expLeaderBoard)
      .setColor('#FF99CC')

    number = 1
    for (const memberFromDb of leaderboard.exp) {
      const member = await interaction.guild.members.fetch(memberFromDb.userID)

      const level = Math.floor(calculateLevelByExp(Number(memberFromDb.experienceInGuild)))
      expEmbed.addFields([{
        name: `#${number} - ${memberName}`,
        value: `Lv. ${level}`,
        inline: true
      }])
      number++
    }

    await interaction.reply({
      embeds: [coinsEmbed, expEmbed]
    })
  } catch (e) {
    console.log(e)
    logger.error('get some error in listen-on-leaderboard.ts')
  }
})
