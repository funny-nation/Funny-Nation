import { client } from '../../client'
import { Interaction } from 'discord.js'
import { createBadge } from './create-badge'
import { buyFromButton, buyFromCommand } from './buy-badge'
import { deleteBadge } from './delete-badge'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (interaction.isCommand()) {
    if (interaction.commandName !== 'badge') return
    const subCommand = interaction.options.getSubcommand()
    switch (subCommand) {
      case 'create':
        await createBadge(interaction)
        return
      case 'buy':
        await buyFromCommand(interaction)
        return
      case 'remove':
        await deleteBadge(interaction)
        return
    }
  }
  if (interaction.isButton()) {
    if (interaction.customId.startsWith('badgeOneClickBuyButton_')) {
      await buyFromButton(interaction)
    }
  }
})
