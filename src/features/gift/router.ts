import { client } from '../../client'
import { Interaction } from 'discord.js'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'
import { createGift } from './create-gift'
import { removeGift } from './remove-gift'
import { sendGift } from './send-gift'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand() || !interaction.guild) return
  // localization
  const dbGuild = await getDbGuild(interaction.guild.id)
  const language = await getLanguage(dbGuild.languageInGuild)
  if (interaction.commandName !== language.gift.command.name) return
  const subCommand = interaction.options.getSubcommand()
  switch (subCommand) {
    case language.gift.command.createGift.name:
      await createGift(interaction, language, dbGuild)
      break
    case language.gift.command.sendGift.name:
      await sendGift(interaction, language, dbGuild)
      break
    case language.gift.command.removeGift.name:
      await removeGift(interaction, language, dbGuild)
      break
    default:
  }
})
