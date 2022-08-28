import { CommandInteraction } from 'discord.js'
import { buyHandler } from './buy-handler'
import { getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

const buyFromCommand = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  if (!guild) return

  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge.commands

  const badgeID = Number(interaction.options.getString(language.badge))
  const autoRenew = interaction.options.getBoolean(language.buy.autoRenew)

  if (isNaN(badgeID) || autoRenew === null) return

  await buyHandler(interaction, badgeID, autoRenew)
}

export { buyFromCommand }
