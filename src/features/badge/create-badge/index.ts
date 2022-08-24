import {
  CommandInteraction,
  GuildMember,
  MessageActionRow,
  MessageButton,
  MessageEmbed
} from 'discord.js'
import { DBBadge } from '../../../models/db-badge'
import { getEmojiIDFromStr, isAdmin, replyOnlyInteractorCanSee } from '../../../utils'
import { resetBadgeChoice } from '../utils/reset-badge-choice'
import { badgeUpdateLock } from '../badge-update-lock'

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
    replyOnlyInteractorCanSee(interaction, 'You dont have permission')
    return
  }

  if (badgeUpdateLock.isLock(guild.id)) {
    replyOnlyInteractorCanSee(interaction, 'Please wait for 1 minute then add your gift')
    return
  }

  if (await DBBadge.countBadgesInGuild(guild.id) > 19) {
    replyOnlyInteractorCanSee(interaction, 'Too many badges')
    return
  }

  const emojiID = getEmojiIDFromStr(emojiStr)

  if (!emojiID) {
    replyOnlyInteractorCanSee(interaction, 'Emoji Invalid')
    return
  }
  let emoji
  try {
    emoji = await guild.emojis.fetch(emojiID)
  } catch (e) {
    replyOnlyInteractorCanSee(interaction, 'Emoji does not existed in this server')
    return
  }

  const dbBadge = await DBBadge.create(name, emojiStr, description, price, tag.id, guild.id)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, 'Badge existed')
    return
  }
  await resetBadgeChoice(guild)

  badgeUpdateLock.lock(guild.id)

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
