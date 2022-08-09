import { client } from '../../../client'
import { Interaction } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId !== 'cardDealerCloseButton') return

  const tabletop = getTabletop(interaction.channelId)

  if (!tabletop) {
    await interaction.update({
      content: '^^',
      components: [],
      embeds: []
    })
    return
  }

  tabletop.destroy()

  if (tabletop.owner !== interaction.member) {
    if (interaction.channel) {
      await interaction.channel.send(interaction.user.username + '你不是该游戏拥有者，无法关闭此次游戏')
    }
    return
  }

  tabletop.destroy()

  await interaction.update({
    content: '^^',
    components: [],
    embeds: []
  })
})
