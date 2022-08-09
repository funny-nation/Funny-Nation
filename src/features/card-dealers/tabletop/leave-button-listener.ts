import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId.length < 25) return

  if (interaction.customId.slice(0, 24) !== 'tabletopKickPlayerButton') return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const tabletop = getTabletop(interaction.channel.id)
  if (!tabletop) return
  const playerId = interaction.customId.slice(24)
  if (interaction.member.id !== playerId) {
    if (tabletop.owner === interaction.member) {
      tabletop.dropPlayer(playerId)
      tabletop.addPlayerToBlacklist(playerId)
      const components = tabletop.renderComponents()

      await interaction.update({
        components
      })
    } else {
      await interaction.channel.send(interaction.member.displayName + ' 您不是房主，无法将别人移除')
    }
    return
  }

  tabletop.dropPlayer(interaction.member.id)

  const components = tabletop.renderComponents()

  await interaction.update({
    components
  })
})
