import { client } from '../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { getDbGuild } from '../../models'
import { getLanguage } from '../../language'
import { logger } from '../../logger'
import { coinTransferHelper } from './transfer-service'
import { TransactionStatus } from './transaction-status'

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
    const language = getLanguage(dbGuild.languageInGuild).transferCoin
    if (interaction.commandName !== language.transferCommand) return

    // Fetching command arguments
    const payee = interaction.options.getUser(language.payee)
    const coinAmount = interaction.options.getInteger(language.coin)
    const detailMsg = interaction.options.getString(language.detail)

    // Compulsory arguments checking
    if (!(payee && coinAmount)) {
      logger.error(`Null payee or coin exception\n${interaction.options}`)
      return
    }

    const payerID = interaction.member.id
    const payeeID = payee.id
    const guildID = interaction.guild.id

    const transferStatus: TransactionStatus = await coinTransferHelper(payerID, payeeID, guildID, coinAmount, detailMsg)
    if (transferStatus === TransactionStatus.INSUFFICIENT_BALANCE) {
      await interaction.reply(language.insufficientBalance)
      return
    }

    if (detailMsg) {
      await interaction.reply({
        content: language.transferCompleteMsg(payee.id, coinAmount),
        embeds: [
          new MessageEmbed()
            .setTitle(detailMsg)
            .setDescription(language.senderLeavingMsgInfo)
        ]
      })
    } else {
      await interaction.reply({
        content: language.transferCompleteMsg(payee.id, coinAmount)
      })
    }
  } catch (e) {
    logger.error('Error occurred in features/slash-command-controller')
    console.error(e)
  }
})
