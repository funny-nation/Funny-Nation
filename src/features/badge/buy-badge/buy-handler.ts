import { ButtonInteraction, CommandInteraction, GuildMember, MessageEmbed } from 'discord.js'
import { DBBadge, DBMemberBadge } from '../../../models/db-badge'
import { getEmojiIDFromStr, replyOnlyInteractorCanSee } from '../../../utils'
import { addDbCoinTransfer, getDbGuild, getDbMember } from '../../../models'
import moment from 'moment-timezone'

const buyHandler = async (interaction: CommandInteraction | ButtonInteraction, badgeID: number, autoRenew: boolean) => {
  const user = interaction.user
  const guild = interaction.guild
  const member = interaction.member
  const currentChannel = interaction.channel

  if (isNaN(badgeID) || !user || !guild || !member || !currentChannel) return

  if (!(member instanceof GuildMember)) return

  const dbBadge = await DBBadge.fetchByID(badgeID)
  if (!dbBadge) {
    replyOnlyInteractorCanSee(interaction, 'Badge not found')
    return
  }
  const emojiID = getEmojiIDFromStr(dbBadge.badgeData.emoji)
  if (!emojiID) {
    replyOnlyInteractorCanSee(interaction, 'Badge emoji not found')
    return
  }
  const emoji = await guild.emojis.fetch(emojiID)

  const dbMember = await getDbMember(user.id, guild.id)
  if (dbBadge.badgeData.price > dbMember.coinBalanceInGuild) {
    replyOnlyInteractorCanSee(interaction, 'You have not enough money')
    return
  }
  const price = Number(dbBadge.badgeData.price)
  await dbMember.reduceCoins(price)
  await addDbCoinTransfer(user.id, guild.id, -price, null, '', 'buyBadge')
  const dbMemberBadge = await DBMemberBadge.buyBadge(dbBadge.badgeData.id, user.id, guild.id, autoRenew)
  const dbGuild = await getDbGuild(guild.id)
  const expireTimeString = moment(dbMemberBadge.data.expiredAt).tz(dbGuild.timeZone).format('YYYY - MM - DD')
  try {
    await member.roles.add(dbBadge.badgeData.roleIDRelated)
  } catch (e) {
    const msg = await currentChannel.send('Due to lack of permission, I cannot put this tag on you. ')
    setTimeout(async () => {
      await msg.delete()
    }, 20000)
  }
  replyOnlyInteractorCanSee(interaction, {
    embeds: [
      new MessageEmbed()
        .setTitle('Purchase success')
        .setDescription(`Your "${dbBadge.badgeData.name}" will be expired in ${expireTimeString}`)
        .addFields({
          name: 'Auto-renew',
          value: autoRenew ? 'Yes' : 'Nop'
        })
        .setColor('#FF99CC')
        .setThumbnail(emoji.url)
    ]
  })
}

export { buyHandler }
