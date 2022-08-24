import { CommandInteraction } from 'discord.js'
import { buyHandler } from './buy-handler'

const buyFromCommand = async (interaction: CommandInteraction) => {
  const badgeID = Number(interaction.options.getString('badge'))
  const autoRenew = interaction.options.getBoolean('auto-renew')

  if (isNaN(badgeID) || autoRenew === null) return

  await buyHandler(interaction, badgeID, autoRenew)
}

export { buyFromCommand }
