import { client } from '../../client'
import { Interaction } from 'discord.js'
import { createBadge } from './create-badge'
import { buyFromButton, buyFromCommand } from './buy-badge'
import { deleteBadge } from './delete-badge'
import { badgeAutoRenewToggleButtonListener, getManageMyBadgePanel } from './manage-my-badge'
import { listAllBadges } from './list-all-badges'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    const guild = interaction.guild
    if (!guild) return

    const dbGuild = await getDbGuild(guild.id)
    const language = getLanguage(dbGuild.languageInGuild).badge.commands

    if (interaction.isCommand()) {
      if (interaction.commandName !== language.name) return
      const subCommand = interaction.options.getSubcommand()
      switch (subCommand) {
        case language.create.name:
          await createBadge(interaction)
          return
        case language.buy.name:
          await buyFromCommand(interaction)
          return
        case language.remove.name:
          await deleteBadge(interaction)
          return
        case language.manageMyBadge.name:
          await getManageMyBadgePanel(interaction)
          return
        case language.list.name:
          await listAllBadges(interaction)
          return
      }
    }
    if (interaction.isButton()) {
      if (interaction.customId.startsWith('badgeOneClickBuyButton_')) {
        await buyFromButton(interaction)
      } else if (interaction.customId.startsWith('badgeAutoRenewToggleButton:')) {
        await badgeAutoRenewToggleButtonListener(interaction)
      }
    }
  } catch (e) {
    logger.error('Error in Badge')
    console.log(e)
  }
})
