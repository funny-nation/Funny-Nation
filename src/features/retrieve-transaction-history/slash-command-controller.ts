import { client } from '../../client'
import { GuildMember, Interaction } from 'discord.js'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    // interactionCreate filtering
    if (
      !interaction.isCommand() ||
      interaction.guild === null ||
      interaction.member === null ||
      !(interaction.member instanceof GuildMember)
    ) return

    // Fetching user's language
    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)

    // command filter
    if (interaction.commandName !== 'retrieveTransactionHistory') return

    await interaction.reply('')
  } catch (e) {
    console.log(e)
  }
})
