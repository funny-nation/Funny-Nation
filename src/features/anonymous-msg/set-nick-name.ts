import { client } from '../../client'
import { Interaction } from 'discord.js'
import { getDbGuild, getDbUser } from '../../models'
import { getLanguage } from '../../language'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand()) return
    if (!interaction.guild) return
    if (!interaction.user) return

    if (interaction.commandName !== 'anonymous') return
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (interaction.options.getSubcommand() !== language.anonymousMsg.commands.setName.name) return
    const nickName = interaction.options.getString(language.anonymousMsg.commands.setName.optionName)
    if (!nickName) return

    const dbUser = await getDbUser(interaction.user.id)
    await dbUser.setAnonymousNickName(nickName)
    await interaction.deferReply({ ephemeral: true })
    await interaction.editReply(`${language.anonymousMsg.yourNewNameIs}\`${nickName}\``)
  } catch (e) {
    logger.error('Error when user setting the anonymous message nickname')
    console.log(e)
  }
})
