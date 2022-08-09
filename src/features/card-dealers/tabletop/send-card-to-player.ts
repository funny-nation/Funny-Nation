import { client } from '../../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId !== 'cardDealerStartButton') return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const tabletop = getTabletop(interaction.channel.id)
  if (!tabletop) return

  if (tabletop.owner !== interaction.member) {
    await interaction.channel.send('只有房主可以开始游戏')
    return
  }

  if (tabletop.maxNumberPlayer > tabletop.players.size) {
    await interaction.channel.send('这局人还没满，再等等等吧！')
    return
  }
  const cards: string[] = []
  for (const cds of tabletop.cards) {
    while (cds.count > 0) {
      cards.push(cds.cardName)
      cds.count -= 1
    }
  }

  const shuffledCards: string[] = cards.sort(() => Math.random() - 0.5)

  for (const [, player] of tabletop.players) {
    const cardName = shuffledCards.pop()
    if (!cardName) break
    await player.member.send({
      embeds: [
        new MessageEmbed()
          .setTitle(cardName)
          .setDescription('>_<')
          .setColor('#FF99CC')
      ]
    })
  }
  tabletop.destroy()

  await interaction.update({
    content: '发牌结束，祝您玩得开心',
    components: [],
    embeds: []
  })
})
