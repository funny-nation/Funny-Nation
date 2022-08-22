import { CommandInteraction, GuildMember, MessageActionRow, MessageButton, MessageEmbed } from 'discord.js'
import { DBBadge } from '../../../models/db-badge'
import { getEmojiIDFromStr, isAdmin } from '../../../utils'

const createBadge = async (interaction: CommandInteraction) => {
  const name = interaction.options.getString('name')
  const emojiStr = interaction.options.getString('emoji')
  const description = interaction.options.getString('description')
  const price = interaction.options.getInteger('price')
  const tag = interaction.options.getRole('tag')
  const guild = interaction.guild
  const member = interaction.member

  if (!(member instanceof GuildMember)) return

  if (
    !name ||
    !emojiStr ||
    !description ||
    !price ||
    !tag ||
    !guild ||
    !member
  ) return

  if (!await isAdmin(member)) {
    await interaction.reply('You dont have permission')
    return
  }

  const emojiID = getEmojiIDFromStr(emojiStr)

  if (!emojiID) {
    await interaction.reply('Emoji Invalid')
    return
  }
  let emoji
  try {
    emoji = await guild.emojis.fetch(emojiID)
  } catch (e) {
    await interaction.reply('Emoji does not existed in this server')
    return
  }

  const dbBadge = await DBBadge.create(name, emojiStr, description, price, tag.id, guild.id)
  if (!dbBadge) {
    await interaction.reply('Badge existed')
    return
  }
  await interaction.reply({
    embeds: [
      new MessageEmbed()
        .setTitle(name)
        .setDescription(`New badge "${name}" has been created. \nClick the button below to buy it. `)
        .setColor('#FF99CC')
        .setFields(
          {
            name: 'Price (coins per month)', value: String(price)
          },
          {
            name: '-', value: description
          }
        )
        .setThumbnail(emoji.url)
    ],
    components: [
      new MessageActionRow()
        .addComponents(
          new MessageButton()
            .setCustomId(`badgeOneClickBuyButton${dbBadge.badgeData.id}`)
            .setLabel('Buy it now')
            .setStyle('SUCCESS')
        )
    ]
  })
}

export { createBadge }
