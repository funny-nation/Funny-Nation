import { ButtonInteraction, CommandInteraction, GuildMember, MessageEmbed } from 'discord.js'
import { DBBadge, DBMemberBadge } from '../../../models/db-badge'
import { getEmojiIDFromStr, replyOnlyInteractorCanSee } from '../../../utils'
import { addDbCoinTransfer, getDbGuild, getDbMember } from '../../../models'
import moment from 'moment-timezone'
import { getLanguage } from '../../../language'

const buyHandler = async (interaction: CommandInteraction | ButtonInteraction, badgeID: number, autoRenew: boolean) => {
  const user = interaction.user
  const guild = interaction.guild
  const member = interaction.member
  const currentChannel = interaction.channel

  if (isNaN(badgeID) || !user || !guild || !member || !currentChannel) return

  if (!(member instanceof GuildMember)) return
  const dbGuild = await getDbGuild(guild.id)
  const language = getLanguage(dbGuild.languageInGuild).badge

  const dbBadge = await DBBadge.fetchByID(badgeID)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, language.badgeNotFound)
    return
  }
  const emojiID = getEmojiIDFromStr(dbBadge.badgeData.emoji)
  if (!emojiID) {
    replyOnlyInteractorCanSee(interaction, language.badgeEmojiNotFound)
    return
  }
  const emoji = await guild.emojis.fetch(emojiID)

  const dbMember = await getDbMember(user.id, guild.id)
  if (dbBadge.badgeData.price > dbMember.coinBalanceInGuild) {
    replyOnlyInteractorCanSee(interaction, language.youHaveNoEnoughMoney)
    return
  }
  const price = Number(dbBadge.badgeData.price)
  await dbMember.reduceCoins(price)
  await addDbCoinTransfer(user.id, guild.id, -price, null, '', 'buyBadge')
  const dbMemberBadge = await DBMemberBadge.buyBadge(dbBadge.badgeData.id, user.id, guild.id, autoRenew)
  const expireTimeString = moment(dbMemberBadge.data.expiredAt).tz(dbGuild.timeZone).format('YYYY - MM - DD')
  try {
    await member.roles.add(dbBadge.badgeData.roleIDRelated)
  } catch (e) {
    const msg = await currentChannel.send(language.youDontHavePermission)
    setTimeout(async () => {
      await msg.delete()
    }, 20000)
  }
  replyOnlyInteractorCanSee(interaction, {
    embeds: [
      new MessageEmbed()
        .setTitle(language.purchaseSuccess)
        .setDescription(language.YourBadgeWillBeExpiredIn(dbBadge.badgeData.name, expireTimeString))
        .addFields({
          name: language.autoRenew,
          value: autoRenew ? language.yes : language.no
        })
        .setColor('#FF99CC')
        .setThumbnail(emoji.url)
    ]
  })
}

export { buyHandler }
