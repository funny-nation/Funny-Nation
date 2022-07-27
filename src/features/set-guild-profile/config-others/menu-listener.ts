import { client } from '../../../client'
import { GuildMember, Interaction, Message } from 'discord.js'
import { getDbGuild, LanguageEnum } from '../../../models'
import moment from 'moment-timezone'
import { isAdmin } from '../../../utils'
import { setUpCommandsForGuild } from '../../../commands-manager'

/**
 * Listen on menu
 */
client.on('interactionCreate', async (interaction: Interaction) => {
  if (
    !interaction.isSelectMenu() ||
    interaction.guild === null ||
    interaction.member === null ||
    !(interaction.member instanceof GuildMember) ||
    !(interaction.message instanceof Message)
  ) return

  if (!await isAdmin(interaction.member)) return
  const dbGuild = await getDbGuild(interaction.guild.id)

  switch (interaction.customId) {
    case 'guildLanguageSettingMenu': {
      const languageUpdatedAt = dbGuild.commandsUpdatedAt
      const nowTime = moment.utc().toDate()
      const timeDeltaInMS = nowTime.getTime() - languageUpdatedAt.getTime()
      if (timeDeltaInMS < 60000) {
        await interaction.message.edit({
          content: 'You can\'t update so frequently; please update that after 1 minute',
          components: []
        })
        return
      }
      const result = interaction.values.toString()
      await dbGuild.setLanguageInGuild(result as LanguageEnum)
      await setUpCommandsForGuild(dbGuild.languageInGuild, interaction.guild)
      await interaction.update({
        content: `Server language has been set to ${result}`,
        components: []
      })

      return
    }
    case 'guildTimeZoneSettingMenu': {
      const result = interaction.values.toString()
      await dbGuild.setTimeZone(result)
      await interaction.update(`Server time zone has been set to ${result}`)
    }
  }
})
