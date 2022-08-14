import { client } from '../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { getDbGuild } from '../../models'
import { retrieveFirst10Transaction } from './service'
import { CoinTransfer } from '@prisma/client'
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
    const { id, languageInGuild, timeZone } = await getDbGuild(interaction.guild.id)
    const language = getLanguage(languageInGuild).transactionsHistory

    // command filter
    if (interaction.commandName !== language.commandName) return

    const transactions: CoinTransfer[] = await retrieveFirst10Transaction(interaction.member.user.id, id)
    const embed = new MessageEmbed()
      .setTitle(language.transactionHistoryTitle)
      .setColor('#FF99CC')
    for (const transaction of transactions) {
      embed.addFields([language.fieldEntry(transaction, timeZone)])
    }
    await interaction.reply({
      embeds: [embed]
    })
  } catch (e) {
    console.log(e)
  }
})
