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

    if (interaction.customId.length < 25) return

    if (interaction.customId.slice(0, 24) !== 'tabletopKickPlayerButton') return

    if (!interaction.channel) return

    if (!(interaction.member instanceof GuildMember)) return
    if (!interaction.guild) return

    const tabletop = getTabletop(interaction.channel.id)
    if (!tabletop) {
      await cleanTable(interaction)
      return
    }

    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    const buttonId = interaction.customId.slice(24)
    if (interaction.member.id !== buttonId) {
      if (tabletop.owner === interaction.member) {
        tabletop.dropPlayer(buttonId)
        tabletop.addPlayerToBlacklist(buttonId)
        const components = tabletop.renderComponents()

        await interaction.update({
          components
        })
      } else {
        replyOnlyInteractorCanSee(interaction, interaction.member.displayName + language.tabletopRoleAssign.kickOutError)
        // await interaction.reply(interaction.member.displayName + language.tabletopRoleAssign.kickOutError)
      }
    } else {
      tabletop.dropPlayer(interaction.member.id)

      const components = tabletop.renderComponents()

      await interaction.update({
        components
      })
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when a user using close button')
  }
})
