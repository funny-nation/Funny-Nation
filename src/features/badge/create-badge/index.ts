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
import { getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

const createBadge = async (interaction: CommandInteraction) => {
  const guild = interaction.guild
  const member = interaction.member
  if (!guild) return
  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge

  const name = interaction.options.getString(language.commands.create.badgeNameOption)
  const emojiStr = interaction.options.getString(language.commands.create.emojiOption)
  const description = interaction.options.getString(language.commands.create.descOption)
  const price = interaction.options.getInteger(language.commands.create.priceOption)
  const tag = interaction.options.getRole(language.commands.create.tagOption)

  if (!(member instanceof GuildMember)) return

  if (
    !name ||
    !emojiStr ||
    !description ||
    !price ||
    !tag ||
    !member
  ) return

  if (!await isAdmin(member)) {
    replyOnlyInteractorCanSee(interaction, language.youDontHavePermission)
    return
  }

  if (badgeUpdateLock.isLock(guild.id)) {
    replyOnlyInteractorCanSee(interaction, language.waitForOneMinuteForAddBadge)
    return
  }

  if (await DBBadge.countBadgesInGuild(guild.id) > 19) {
    replyOnlyInteractorCanSee(interaction, language.tooManyBadges)
    return
  }

  const emojiID = getEmojiIDFromStr(emojiStr)

  if (!emojiID) {
    replyOnlyInteractorCanSee(interaction, language.emojiInvalid)
    return
  }
  let emoji
  try {
    emoji = await guild.emojis.fetch(emojiID)
  } catch (e) {
    replyOnlyInteractorCanSee(interaction, language.emojiDoesNotExistHere)
    return
  }

  const dbBadge = await DBBadge.create(name, emojiStr, description, price, tag.id, guild.id)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, language.badgeExisted)
    return
  }
  await resetBadgeChoice(guild)

  badgeUpdateLock.lock(guild.id)

  await interaction.reply({
    embeds: [
      new MessageEmbed()
        .setTitle(name)
        .setDescription(language.NewBadgeHasBeenCreated(name))
        .setColor('#FF99CC')
        .setFields(
          {
            name: language.priceCoinsPerMonth, value: String(price)
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
            .setLabel(language.buyItNow)
            .setStyle('SUCCESS')
        )
    ]
  })
}

export { createBadge }
