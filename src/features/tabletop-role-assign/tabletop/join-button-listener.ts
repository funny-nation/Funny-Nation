import { client } from '../../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getTabletop } from './storage'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'
import { cleanTable } from './utils/cleanTable'
import { logger } from '../../../logger'
import { replyOnlyInteractorCanSee } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isButton()) return

    if (interaction.customId !== 'roleAssignJoinButton') return

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
    if (tabletop.blacklists.indexOf(interaction.member.id) !== -1) {
      replyOnlyInteractorCanSee(interaction, interaction.member.displayName + language.tabletopRoleAssign.kickOutByOwner)
      // await interaction.reply(interaction.member.displayName + language.tabletopRoleAssign.kickOutByOwner)
      return
    }
    if (tabletop.maxNumberPlayer <= tabletop.players.size) {
      replyOnlyInteractorCanSee(interaction, interaction.member.displayName + language.tabletopRoleAssign.fullOfPeople)
      // await interaction.reply(interaction.member.displayName + language.tabletopRoleAssign.fullOfPeople)
      return
    }

    tabletop.addPlayer(interaction.member)

    const components = tabletop.renderComponents()

    await interaction.update({
      components
    })
  } catch (e) {
    console.log(e)
    logger.error('Error when a user using close button')
  }
})
