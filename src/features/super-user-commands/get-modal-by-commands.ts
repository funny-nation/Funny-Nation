import { client } from '../../client'
import { Interaction } from 'discord.js'
import { getSuperUserNotificationModal } from './factory/get-super-user-notification-modal'
import { LanguageEnum } from '../../models'
import { superUserID } from './super-user-id-from-env'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand()) return

    if (interaction.commandName !== 'superuser') return

    if (!superUserID) return

    if (interaction.user.id !== superUserID) return

    const subcommand = interaction.options.getSubcommand()
    if (subcommand === null) return

    switch (subcommand) {
      case 'demo-notification': {
        const modal = getSuperUserNotificationModal('superuser-notification-demo-modal')
        await interaction.showModal(modal)
        return
      }
      case 'send-notification': {
        const language = interaction.options.getString('language')
        const modal = getSuperUserNotificationModal('superuser-notification-send-modal', language as LanguageEnum)
        await interaction.showModal(modal)
      }
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when a super user request a modal')
  }
})
