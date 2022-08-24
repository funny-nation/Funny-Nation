import { DBBadge } from '../../../models/db-badge'
import { ApplicationCommandOptionChoiceData, Guild } from 'discord.js'
import { updateCommandOptionChoicesForGuild } from '../../../utils'

const resetBadgeChoice = async (guild: Guild) => {
  const badgeList = await DBBadge.fetchManyByGuild(guild.id)
  const newOptions: ApplicationCommandOptionChoiceData[] = []
  for (const badgeFromList of badgeList) {
    newOptions.push({
      name: badgeFromList.badgeData.name,
      value: String(badgeFromList.badgeData.id)
    })
  }
  await updateCommandOptionChoicesForGuild(guild, 'badge', 'remove', 'badge', newOptions)
  await updateCommandOptionChoicesForGuild(guild, 'badge', 'buy', 'badge', newOptions)
}

export { resetBadgeChoice }
