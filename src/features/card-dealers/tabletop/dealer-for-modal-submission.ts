import { client } from '../../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { Card } from './types/card'
import { newTabletop } from './storage'
import { getProcessControlActionRow } from './get-process-control-action-row'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isModalSubmit()) return

  if (interaction.customId !== 'dealerModalSubmission') return

  const rolesInput = interaction.fields.getTextInputValue('input')

  if (!rolesInput) return
  if (!interaction.member) return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const roles: string[] = rolesInput.split('\n')
  const cards: Card[] = []
  let totalNumberOfPlayer = 0
  for (const role of roles) {
    if (role === '') continue
    const cardNameNumber = role.split(/[：:]/)
    if (cardNameNumber.length !== 2) continue
    const number = parseInt(cardNameNumber[1])
    if (isNaN(number)) continue
    cards.push({
      cardName: cardNameNumber[0],
      count: number
    })
    totalNumberOfPlayer += number
  }
  if (cards.length < 2) {
    await interaction.reply('只设置一个类型的牌玩不起来啊')
    return
  }

  const tabletop = newTabletop(interaction.channel, cards, interaction.member, totalNumberOfPlayer)

  if (!tabletop) {
    await interaction.reply('Channel has been used')
    return
  }

  const embedMsg = new MessageEmbed()
    .setTitle(`来自 ${interaction.member.displayName}`)
    .setColor('#FF99CC')
    .setDescription('的发牌器')

  for (const card of tabletop.cards) {
    embedMsg.addField(card.cardName, `${card.count}个`)
  }

  await interaction.reply({
    embeds: [embedMsg],
    components: [getProcessControlActionRow()]
  })
})
