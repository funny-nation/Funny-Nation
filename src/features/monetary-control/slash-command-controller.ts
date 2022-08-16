import { client } from '../../client'
import { GuildMember, Interaction } from 'discord.js'
import { collectCoinsFromUser, issueCoinsToUser } from './service'
import { logger } from '../../logger'
import { isAdmin } from '../../utils'
import { getLanguage } from '../../language'
import { getDbGuild } from '../../models'

client.on('interactionCreate', async (interaction: Interaction) => {
  const guild = interaction.guild
  const member = interaction.member
  try {
    if (
      !interaction.isCommand() || guild === null || !(member instanceof GuildMember)
    ) return

    const dbGuild = await getDbGuild(guild.id)
    const language = getLanguage(dbGuild.languageInGuild).monetaryControl
    const commandName = interaction.commandName
    const options = interaction.options
    if (commandName !== language.coinCommand) return

    const isAdministrator = await isAdmin(member)
    if (!isAdministrator) {
      await interaction.reply(language.notAdministratorMsg)
      return
    }
    const amount = options.getInteger(language.amountOption)
    const targetUser = options.getUser(language.targetUserOption)

    if (amount == null || targetUser == null) {
      logger.error('null value of amount/targetUser')
      return
    }

    switch (options.getSubcommand()) {
      case language.collectSubcommand:
        await collectCoinsFromUser(guild.id, targetUser.id, amount)
        await interaction.reply(language.collectedSuccessInfo(targetUser, amount))
        return
      case language.issueSubcommand:
        await issueCoinsToUser(guild.id, targetUser.id, amount)
        await interaction.reply(language.issuedSuccessInfo(targetUser, amount))
        return
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when administrator collect or issue coins')
  }
})
