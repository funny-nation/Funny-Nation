import { ButtonInteraction } from 'discord.js'
import { replyOnlyInteractorCanSee } from '../../../../utils'
import { DBGuild, getDbGuild } from '../../../../models'
import { getLanguage } from '../../../../language'

const cleanTable = async (interaction: ButtonInteraction) => {
  if (!interaction.guild) return
  const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.gameClosed)
  // await interaction.update({
  //   content: '^^',
  //   components: [],
  //   embeds: []
  // })
}

export { cleanTable }
