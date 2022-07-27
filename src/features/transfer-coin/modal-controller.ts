import { client } from '../../client'
import {
  GuildMember,
  Interaction,
  MessageActionRow,
  Modal,
  ModalActionRowComponent,
  TextInputComponent
} from 'discord.js'
import { getLanguage } from '../../language'
import { TextInputStyles } from 'discord.js/typings/enums'
import { getDbGuild } from '../../models'
import { coinTransferHelper } from './transfer-service'
import { TransactionStatus } from './transaction-status'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (
    !interaction.isUserContextMenu() ||
    interaction.guild === null ||
    interaction.member === null ||
    !(interaction.member instanceof GuildMember)
  ) return

  // Fetching user's language
  const dbGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild).transferCoin
  if (interaction.commandName !== language.commandLang) return

  const modal = new Modal()
    .setTitle(language.commandLang)
    .setCustomId(`transferringModal${interaction.targetUser.id}`)
  const amountComponent = new TextInputComponent()
    .setLabel(language.coinDesc)
    .setRequired(true)
    .setCustomId('amountInput')
    .setStyle(TextInputStyles.SHORT)
    .setPlaceholder('Integer only')
  const remarksComponent = new TextInputComponent()
    .setLabel(language.detail)
    .setCustomId('remarksComponent')
    .setStyle(TextInputStyles.PARAGRAPH)
    .setPlaceholder(language.detailDesc)

  modal.addComponents(
    new MessageActionRow<ModalActionRowComponent>().addComponents(amountComponent),
    new MessageActionRow<ModalActionRowComponent>().addComponents(remarksComponent)
  )
  await interaction.showModal(modal)
})

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isModalSubmit()) return
  if (interaction.guild === null) return
  if (!interaction.customId.startsWith('transferringModal')) return
  // Fetching user's language
  const dbGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild).transferCoin

  const payerID = interaction.user.id
  const payeeID = interaction.customId.substring(17)
  const guildID = interaction.guild.id
  const amount = parseInt(interaction.fields.getField('amountInput').value)
  const desc: string = interaction.fields.getField('remarksComponent').value
  if (!amount) {
    await interaction.reply('invalid amount of coin')
    return
  }
  console.log(`payerID: ${payerID} payeeID: ${payeeID} amount: ${amount}, guild: ${guildID}`)
  const status = await coinTransferHelper(payerID, payeeID, guildID, amount, desc || null)
  if (status === TransactionStatus.INSUFFICIENT_BALANCE) {
    await interaction.update(language.insufficientBalance)
    return
  }
  await interaction.reply(language.transferCompleteMsg(payeeID, amount))
})
