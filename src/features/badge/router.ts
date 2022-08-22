import { client } from '../../client'
import { Interaction } from 'discord.js'
import { createBadge } from './create-badge'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return
  if (interaction.commandName !== 'badge') return
  const subCommand = interaction.options.getSubcommand()
  switch (subCommand) {
    case 'create':
      await createBadge(interaction)
  }
})
