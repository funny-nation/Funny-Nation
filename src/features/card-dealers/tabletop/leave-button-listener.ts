import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId !== 'tabletopKickPlayerButton' + interaction.user.id) return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const tabletop = getTabletop(interaction.channel.id)
  if (!tabletop) return

  tabletop.dropPlayer(interaction.member.id)

  const components = tabletop.renderComponents()

  await interaction.update({
    components
  })
})
