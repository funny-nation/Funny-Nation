import {
  ApplicationCommandOptionChoiceData,
  CommandInteraction,
  GuildMember,
  MessageActionRow,
  MessageButton,
  MessageEmbed
} from 'discord.js'
import { DBBadge } from '../../../models/db-badge'
import { getEmojiIDFromStr, isAdmin, updateCommandOptionChoicesForGuild } from '../../../utils'
import { wait } from '../../../utils/wait'

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
    await wait(20000)
    await interaction.deleteReply()
    return
  }

  if (await DBBadge.countBadgesInGuild(guild.id) > 19) {
    await interaction.reply('Too many badges')
    await wait(20000)
    await interaction.deleteReply()
    return
  }

  const emojiID = getEmojiIDFromStr(emojiStr)

  if (!emojiID) {
    await interaction.reply('Emoji Invalid')
    await wait(20000)
    await interaction.deleteReply()
    return
  }
  let emoji
  try {
    emoji = await guild.emojis.fetch(emojiID)
  } catch (e) {
    await interaction.reply('Emoji does not existed in this server')
    await wait(20000)
    await interaction.deleteReply()
    return
  }

  const dbBadge = await DBBadge.create(name, emojiStr, description, price, tag.id, guild.id)
  if (!dbBadge) {
    await interaction.reply('Badge existed')
    await wait(20000)
    await interaction.deleteReply()
    return
  }
  const badgeList = await DBBadge.fetchManyByGuild(guild.id)
  const newOptions: ApplicationCommandOptionChoiceData[] = []
  for (const badgeFromList of badgeList) {
    newOptions.push({
      name: badgeFromList.badgeData.name,
      value: String(badgeFromList.badgeData.id)
    })
  }
  await updateCommandOptionChoicesForGuild(guild, 'badge', 'remove', 'badge', newOptions)
  await updateCommandOptionChoicesForGuild(guild, 'badge', 'buy', 'badge', newOptions)
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
            .setCustomId(`badgeOneClickBuyButton_${dbBadge.badgeData.id}`)
            .setLabel('Buy it now')
            .setStyle('SUCCESS')
        )
    ]
  })
}

export { createBadge }
