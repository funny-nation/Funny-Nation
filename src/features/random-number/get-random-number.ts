import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return
  if (interaction.commandName !== 'random-number') return
  if (!interaction.guild) return
  const minNum = Math.min(interaction.options.getInteger('第一个数') as number, interaction.options.getInteger('第二个数') as number)
  const maxNum = Math.max(interaction.options.getInteger('第一个数') as number, interaction.options.getInteger('第二个数') as number)
  const range = interaction.options.getInteger('生成个数') as number
  const randomNumberList = []

  if (minNum === maxNum) {
    if (interaction.channel) {
      await interaction.reply('您的第一个数和第二个数不能一样')
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
  console.log(randomNumberList.toString())

  const embedMsg = new MessageEmbed()
    .setTitle('您生成的随机数是')
    .setColor('#FF99CC')
    .setDescription(randomNumberList.toString())

  // for (let i = 0; i <= randomNumberList.length; i++) {
  //   embedMsg.addField(i + ':', randomNumberList[i].toString())
  // }

  await interaction.reply({
    embeds: [embedMsg]
  })
})
