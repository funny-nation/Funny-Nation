import { CommandInteraction, GuildMember } from 'discord.js'
import { Language } from '../../../language'
import { DBGuild } from '../../../models'
import { isAdmin, replyOnlyInteractorCanSee } from '../../../utils'
import { DBGift } from '../../../models/db-gift/creat-gift'
import { updateGiftToOption } from '../helper/update-gift-to-option'

const removeGift = async (interaction: CommandInteraction, language: Language, dbGuild: DBGuild) => {
  const giftName = interaction.options.getString(language.gift.command.removeGift.stringOptionName)
  if (!giftName) return
  if (interaction.commandName !== language.gift.command.name) return
  if (!interaction.member) return
  if (!(interaction.member instanceof GuildMember)) return
  // verify admin user
  const isAdministrator = await isAdmin(interaction.member)
  if (!isAdministrator) {
    await replyOnlyInteractorCanSee(interaction, 'you are not administrator')
    return
  }
  const gift = await DBGift.getGift(giftName, dbGuild.id)
  if (!gift) {
    await replyOnlyInteractorCanSee(interaction, 'gift is not existed')
    return
  }
  await gift.remove()
  await replyOnlyInteractorCanSee(interaction, 'successfully removed gift')
  // update gift to option
  const guildId = dbGuild.id
  const giftList = await DBGift.getGiftList(guildId)
  await updateGiftToOption(giftList, interaction, language)
}

export { removeGift }
