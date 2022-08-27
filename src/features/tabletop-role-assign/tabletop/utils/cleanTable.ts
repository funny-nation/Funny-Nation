import { ButtonInteraction } from 'discord.js'
import { DBGuild, getDbGuild } from '../../../../models'
import { getLanguage } from '../../../../language'

const cleanTable = async (interaction: ButtonInteraction) => {
  if (!interaction.guild) return
  const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  await interaction.update({
    content: language.tabletopRoleAssign.gameClosed,
    components: [],
    embeds: []
  })
}
export { cleanTable }
