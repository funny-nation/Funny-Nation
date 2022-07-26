import { client } from '../../client'
import { Guild, GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { getDbMember, addDbCoinTransfer, getDbGuild } from '../../models'
import { randomUUID } from 'crypto'
import { getLanguage } from '../../language'
import { logger } from '../../logger'
client.on('interactionCreate', async (interaction:Interaction) => {
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
  const coin = interaction.options.getInteger(language.coin)
  const detailMsg = interaction.options.getString(language.detail)

  // Compulsory arguments checking
  if (!(payee && coin)) {
    logger.info(`Null payee or coin exception\n${interaction.options}`)
    return
  }

  // Extracting guild info
  const payer :GuildMember = interaction.member
  const guild: Guild = interaction.guild

  // Fetching payer's and payee's info from database
  const dbMember = await getDbMember(payer.id, guild.id)
  const payeeDbMember = await getDbMember(payee.id, guild.id)

  // Coin balance checking
  if (coin > dbMember.coinBalanceInGuild) {
    await interaction.reply(language.insufficientBalance)
    return
  }
  // Operating in database
  await dbMember.reduceCoins(coin)
  await payeeDbMember.addCoins(coin)
  const transactionID = randomUUID() // Generate a shared UUID for matching a pair of DR & CR records.
  await addDbCoinTransfer(payee.id, guild.id, coin, transactionID, detailMsg || '', 'transferOut')
  await addDbCoinTransfer(payer.id, guild.id, -coin, transactionID, detailMsg || '', 'transferIn')
  // Interaction replying successful transferring message
  if (detailMsg) {
    await interaction.reply({
      content: language.transferCompleteMsg(payee.id, coin),
      embeds: [
        new MessageEmbed()
          .setTitle(detailMsg)
          .setDescription(language.senderLeavingMsgInfo)
      ]
    })
  } else {
    await interaction.reply({
      content: language.transferCompleteMsg(payee.id, coin)
    })
  }
})
