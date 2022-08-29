import { ButtonInteraction } from 'discord.js'
import { buyHandler } from './buy-handler'

const buyFromButton = async (interaction: ButtonInteraction) => {
  const customIDSplit = interaction.customId.split('_')
  if (customIDSplit.length !== 2) return
  const badgeID = Number(customIDSplit[1])
  if (isNaN(badgeID)) return
  await buyHandler(interaction, badgeID, true)
}

export { buyFromButton }
