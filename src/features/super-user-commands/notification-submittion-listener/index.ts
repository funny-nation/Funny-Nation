import { client } from '../../../client'
import { Interaction } from 'discord.js'
import { notificationDemoHandler } from './notification-demo-handler'
import { notificationSendHandler } from './notification-send-handler'
import { superUserID } from '../super-user-id-from-env'
import { logger } from '../../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isModalSubmit()) return
    if (interaction.user.id !== superUserID) return

    switch (interaction.customId) {
      case 'superuser-notification-demo-modal': {
        await notificationDemoHandler(interaction)
        return
      }
      case 'superuser-notification-send-modal': {
        await notificationSendHandler(interaction)
      }
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when receiving data from Modal for sending the notification')
  }
})
