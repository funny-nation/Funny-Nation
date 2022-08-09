import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getTabletop } from './storage'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isButton()) return

  if (interaction.customId !== 'cardDealerJoinButton') return

  if (!interaction.channel) return

  if (!(interaction.member instanceof GuildMember)) return

  const tabletop = getTabletop(interaction.channel.id)
  if (!tabletop) return
  if (tabletop.maxNumberPlayer <= tabletop.players.size) {
    await interaction.channel.send(interaction.member.displayName + ' 这局人满了，等下一局吧！')
    return
  }

  if (tabletop.blacklists.indexOf(interaction.member.id) !== -1) {
    await interaction.channel.send(interaction.member.displayName + ' 您已被踢出，无法再次进入')
    return
  }

  tabletop.addPlayer(interaction.member)

  const components = tabletop.renderComponents()

  await interaction.update({
    components
  })
})
