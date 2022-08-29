import { DBBadge } from '../../../models/db-badge'
import { ApplicationCommandOptionChoiceData, Guild } from 'discord.js'
import { updateCommandOptionChoicesForGuild } from '../../../utils'
import { Language } from '../../../language'

const resetBadgeChoice = async (guild: Guild, language: Language) => {
  const badgeList = await DBBadge.fetchManyByGuild(guild.id)
  const newOptions: ApplicationCommandOptionChoiceData[] = []
  for (const badgeFromList of badgeList) {
    newOptions.push({
      name: badgeFromList.badgeData.name,
      value: String(badgeFromList.badgeData.id)
    })
  }
  await updateCommandOptionChoicesForGuild(guild, language.badge.commands.name, language.badge.commands.remove.name, language.badge.commands.badge, newOptions)
  await updateCommandOptionChoicesForGuild(guild, language.badge.commands.name, language.badge.commands.buy.name, language.badge.commands.badge, newOptions)
}

export { resetBadgeChoice }
