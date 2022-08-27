import { ButtonInteraction, ModalSubmitInteraction } from 'discord.js'
import { DBGuild, getDbGuild } from '../../../../models'
import { getLanguage } from '../../../../language'
import { replyOnlyInteractorCanSee } from '../../../../utils'

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
