import { CommandInteraction, GuildMember } from 'discord.js'
import { isAdmin, replyOnlyInteractorCanSee } from '../../../utils'
import { DBBadge } from '../../../models/db-badge'
import { resetBadgeChoice } from '../utils/reset-badge-choice'
import { badgeUpdateLock } from '../badge-update-lock'

const deleteBadge = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  const member = interaction.member
  const badgeID = Number(interaction.options.getString('badge'))
  if (!member || !guild || isNaN(badgeID)) return
  if (!(member instanceof GuildMember)) return

  if (!await isAdmin(member)) {
    replyOnlyInteractorCanSee(interaction, 'You dont have permission')
    return
  }
  if (badgeUpdateLock.isLock(guild.id)) {
    replyOnlyInteractorCanSee(interaction, 'Please wait for 1 minute')
    return
  }
  const dbBadge = await DBBadge.fetchByID(badgeID)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, 'Badge does not exist')
    return
  }
  await dbBadge.delete()
  badgeUpdateLock.lock(guild.id)
  await resetBadgeChoice(guild)
  replyOnlyInteractorCanSee(interaction, `Badge "${dbBadge.badgeData.name}" is removed; however badge holders would keep their tag. `)
}

export { deleteBadge }
