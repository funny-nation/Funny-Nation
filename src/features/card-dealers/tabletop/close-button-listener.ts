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

  if (tabletop.owner.id !== interaction.user.id) return

  tabletop.destroy()

  await interaction.update({
    content: '^^',
    components: [],
    embeds: []
  })
})
