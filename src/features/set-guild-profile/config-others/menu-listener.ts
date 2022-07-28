import { client } from '../../../client'
import { GuildMember, Interaction, Message } from 'discord.js'
import { getDbGuild, LanguageEnum } from '../../../models'
import moment from 'moment-timezone'
import { isAdmin } from '../../../utils'
import { setUpCommandsForGuild } from '../../../commands-manager'
import { getLanguage } from '../../../language'
import { logger } from '../../../logger'

/**
 * Listen on menu
 */
client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (
      !interaction.isSelectMenu() ||
      interaction.guild === null ||
      interaction.member === null ||
      !(interaction.member instanceof GuildMember) ||
      !(interaction.message instanceof Message)
    ) return

    if (!await isAdmin(interaction.member)) return

    const dbGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)

    switch (interaction.customId) {
      case 'guildLanguageSettingMenu': {
        const languageUpdatedAt = dbGuild.commandsUpdatedAt
        const nowTime = moment.utc().toDate()
        const timeDeltaInMS = nowTime.getTime() - languageUpdatedAt.getTime()
        if (timeDeltaInMS < 60000) {
          await interaction.message.edit({
            content: language.setGuildProfile.languageUpdateSoFrequent,
            components: []
          })
          return
        }
        const result = interaction.values.toString()
        await dbGuild.setLanguageInGuild(result as LanguageEnum)
        await setUpCommandsForGuild(dbGuild.languageInGuild, interaction.guild)
        await interaction.update({
          content: language.setGuildProfile.successMsg.setLanguage(dbGuild.languageInGuild),
          components: []
        })

        return
      }
      case 'guildTimeZoneSettingMenu': {
        const result = interaction.values.toString()
        await dbGuild.setTimeZone(result)
        await interaction.update(language.setGuildProfile.successMsg.setTimeZone(result))
      }
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when configure guild other menu submitted')
  }
})
