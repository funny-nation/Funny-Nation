import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId !== 'cardDealerStartButton') return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const tabletop = getTabletop(interaction.channel.id)
  if (!tabletop) return

  // TODO: send card to each player

  tabletop.destroy()

  const components = tabletop.renderComponents()

  await interaction.update({
    components
  })
})
