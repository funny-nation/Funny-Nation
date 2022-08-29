import { CommandInteraction, GuildMember } from 'discord.js'
import { Language } from '../../../language'
import { DBGuild } from '../../../models'
import { isAdmin } from '../../../utils'
import { DBGift } from '../../../models/db-gift/creat-gift'
import { updateGiftToOption } from '../helper/update-gift-to-option'
import { logger } from '../../../logger'

const removeGift = async (interaction: CommandInteraction, language: Language, dbGuild: DBGuild) => {
  try {
    const giftName = interaction.options.getString(language.gift.command.removeGift.stringOptionName)
    if (!giftName) return
    if (interaction.commandName !== language.gift.command.name) return
    if (!interaction.member) return
    if (!(interaction.member instanceof GuildMember)) return
    // verify admin user
    const isAdministrator = await isAdmin(interaction.member)
    if (!isAdministrator) {
      await interaction.reply({
        content: 'you are not administrator'
      })
      return
    }
    const gift = await DBGift.getGift(giftName, dbGuild.id)
    if (!gift) {
      await interaction.reply('gift is not existed')
      return
    }
    await gift.remove()
    await interaction.reply('successfully removed gift')
    // update gift to option
    const guildId = dbGuild.id
    const giftList = await DBGift.getGiftList(guildId)
    const option = 'remove'
    await updateGiftToOption(giftList, interaction, language, option)
    await interaction.reply({
      content: 'Gift created'
    })
  } catch (e) {
    console.log(e)
    logger.error('error occurs when executing features/gift/remove-gift')
  }
}

export { removeGift }
