import { client } from '../../client'
import { Interaction } from 'discord.js'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'
import { createGift } from './create-gift/creat-gift'
import { removeGift } from './remove-gift'
import { sendGift } from './send-gift'
import { submitModal } from './create-gift/submit-modal'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.guild) return
    // localization
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = await getLanguage(dbGuild.languageInGuild)

    if (interaction.isCommand()) {
      if (interaction.commandName !== language.gift.command.name) return
      const subCommand = interaction.options.getSubcommand()
      switch (subCommand) {
        case language.gift.command.createGift.name:
          await createGift(interaction, language)
          return
        case language.gift.command.sendGift.name:
          await sendGift(interaction, language, dbGuild)
          return
        case language.gift.command.removeGift.name:
          await removeGift(interaction, language, dbGuild)
          return
        default:
      }
    }
    if (interaction.isModalSubmit()) {
      await submitModal(interaction, language, dbGuild)
    }
  } catch (e) {
    console.log(e)
    logger.error('error occurs when executing feature/gift/router')
  }
})
