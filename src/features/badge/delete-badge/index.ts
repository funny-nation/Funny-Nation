import { CommandInteraction, GuildMember } from 'discord.js'
import { isAdmin, replyOnlyInteractorCanSee } from '../../../utils'
import { DBBadge } from '../../../models/db-badge'
import { resetBadgeChoice } from '../utils/reset-badge-choice'
import { badgeUpdateLock } from '../badge-update-lock'
import { getLanguage } from '../../../language'
import { getDbGuild } from '../../../models'

const deleteBadge = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  if (!guild) return
  const member = interaction.member
  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge
  const badgeID = Number(interaction.options.getString(language.commands.badge))
  if (!member || isNaN(badgeID)) return
  if (!(member instanceof GuildMember)) return

  if (!await isAdmin(member)) {
    replyOnlyInteractorCanSee(interaction, language.youDontHavePermission)
    return
  }
  if (badgeUpdateLock.isLock(guild.id)) {
    replyOnlyInteractorCanSee(interaction, language.waitForOneMinuteForAddBadge)
    return
  }
  const dbBadge = await DBBadge.fetchByID(badgeID)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, language.badgeNotFound)
    return
  }
  await dbBadge.delete()
  badgeUpdateLock.lock(guild.id)
  await resetBadgeChoice(guild)
  replyOnlyInteractorCanSee(interaction, language.badgeIsSuccessfullyRemoved(dbBadge.badgeData.name))
}

export { deleteBadge }
