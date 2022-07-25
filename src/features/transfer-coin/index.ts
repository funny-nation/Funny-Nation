import client from '../../client'
import { Guild, GuildMember, Interaction, MessageEmbed } from 'discord.js'
import getDbMember from '../../models/db-member/get-db-member'
import addDbCoinTransfer from '../../models/db-coin-transfer/add-db-coin-transfer'
import { randomUUID } from 'crypto'
client.on('interactionCreate', async (interaction:Interaction) => {
  if (
    !interaction.isCommand() ||
    interaction.guild === null ||
    interaction.member === null ||
    interaction.commandName !== 'transfer'
  ) return
  if (!(interaction.member instanceof GuildMember)) return

  const payee = interaction.options.getUser('payee')
  const coin = interaction.options.getInteger('coin')
  const detailMsg = interaction.options.getString('detail')

  if (payee === null || coin === null) return

  const payer :GuildMember = interaction.member
  const guild: Guild = interaction.guild

  const dbMember = await getDbMember(payer.id, guild.id)
  const payeeDbMember = await getDbMember(payee.id, guild.id)

  if (coin > dbMember.coinBalanceInGuild) {
    await interaction.reply('你没钱')
    return
  }
  await dbMember.reduceCoins(coin)
  await payeeDbMember.addCoins(coin)
  const transactionID = randomUUID()
  await addDbCoinTransfer(payee.id, guild.id, coin, transactionID, detailMsg || '', 'transferOut')
  await addDbCoinTransfer(payer.id, guild.id, -coin, transactionID, detailMsg || '', 'transferIn')
  if (detailMsg) {
    await interaction.reply({
      content: `Transfer complete! <@${payee.id}> You have received the coins. `,
      embeds: [
        new MessageEmbed()
          .setTitle(detailMsg)
          .setDescription('Sender has leave a message to you')
      ]
    })
  } else {
    await interaction.reply({
      content: `Transfer complete! <@${payee.id}> You have received the coins. `
    })
  }
})
