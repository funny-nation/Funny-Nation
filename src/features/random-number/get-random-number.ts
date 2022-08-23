import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { logger } from '../../logger'
import { DBGuild, getDbGuild } from '../../models'
import { getLanguage } from '../../language'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand()) return
    if (interaction.commandName !== 'random-number') return
    if (!interaction.guild) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    const minNum = Math.min(interaction.options.getInteger(language.randomNumber.firstNumberOptionName) as number, interaction.options.getInteger(language.randomNumber.secondNumberOptionName) as number)
    const maxNum = Math.max(interaction.options.getInteger(language.randomNumber.firstNumberOptionName) as number, interaction.options.getInteger(language.randomNumber.secondNumberOptionName) as number)
    const range = interaction.options.getInteger(language.randomNumber.rangeNumberOptionName) as number
    const randomNumberList = []

    if (minNum === maxNum) {
      if (interaction.channel) {
        await interaction.reply(language.randomNumber.minNumberIsMaxNumberError)
      }
      return
    }
    // Turn on this line of code if needed without repeating
    // if (secondNumber - firstNumber < range) {
    //   if (interaction.channel) {
    //     await interaction.reply('生成范围必须小于两数之差')
    //   }
    //   return
    // }

    for (let i = 0; i <= range; i++) {
      randomNumberList.push(Math.floor(Math.random() * (maxNum - minNum + 1) + minNum))
    }
    const embedMsg = new MessageEmbed()
      .setTitle(language.randomNumber.embedMessageTitle)
      .setColor('#FF99CC')
      .setDescription(randomNumberList.toString())

    await interaction.reply({
      embeds: [embedMsg]
    })
  } catch (e) {
    console.log(e)
    logger.error('Error when create random number')
  }
})
