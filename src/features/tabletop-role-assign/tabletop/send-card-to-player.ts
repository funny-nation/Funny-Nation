import { client } from '../../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { getTabletop } from './storage'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'
import { cleanTable } from './utils/cleanTable'
import { logger } from '../../../logger'
import { replyOnlyInteractorCanSee } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isButton()) return

    if (interaction.customId !== 'roleAssignStartButton') return

    if (!interaction.channel) return

    if (!(interaction.member instanceof GuildMember)) return
    if (!interaction.guild) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)

    const tabletop = getTabletop(interaction.channel.id)
    if (!tabletop) {
      await cleanTable(interaction)
      return
    }

    if (tabletop.owner !== interaction.member) {
      replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.onlyOwnerCanStart)
      // await interaction.reply(language.tabletopRoleAssign.onlyOwnerCanStart)
      return
    }

    if (tabletop.maxNumberPlayer > tabletop.players.size) {
      replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.notEnoughPeople)
      // await interaction.reply(language.tabletopRoleAssign.notEnoughPeople)
      return
    }
    const roles: string[] = []
    for (const role of tabletop.roleGroups) {
      while (role.count > 0) {
        roles.push(role.roleName)
        role.count -= 1
      }
    }

    const shuffledCards: string[] = roles.sort(() => Math.random() - 0.5)

    for (const [, player] of tabletop.players) {
      const cardName = shuffledCards.pop()
      if (!cardName) break
      await player.member.send({
        embeds: [
          new MessageEmbed()
            .setTitle(cardName)
            .setDescription('>_<')
            .setColor('#FF99CC')
        ]
      })
    }
    tabletop.destroy()

    await interaction.update({
      content: language.tabletopRoleAssign.endTabletop,
      components: [],
      embeds: []
    })
  } catch (e) {
    console.log(e)
    logger.error('Error when a user using close button')
  }
})
