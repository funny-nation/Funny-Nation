import { CommandInteraction, MessageEmbed, Role } from 'discord.js'
import { DBBadge } from '../../../models/db-badge'
import { replyOnlyInteractorCanSee } from '../../../utils'
import { logger } from '../../../logger'

const listAllBadges = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  if (!guild) return

  const dbBadges = await DBBadge.fetchManyByGuild(guild.id)
  const embed = new MessageEmbed()
    .setTitle('Badges in this server')
    .setDescription('Here are the badges for you to buy')
    .setColor('#FF99CC')

  for (const dbBadge of dbBadges) {
    const emojiStr = dbBadge.badgeData.emoji
    let role: Role | null = null
    try {
      role = await guild.roles.fetch(dbBadge.badgeData.roleIDRelated)
    } catch (e) {
      logger.verbose('Role missing')
    }

    embed.addFields({
      name: `${emojiStr} ${dbBadge.badgeData.name} - ${dbBadge.badgeData.price}`,
      value: role ? `${role} \n ${dbBadge.badgeData.desc} \n -` : `${dbBadge.badgeData.desc} \n -`
    })
  }

  replyOnlyInteractorCanSee(interaction, {
    embeds: [
      embed
    ]
  })
}

export { listAllBadges }
