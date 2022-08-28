import { DBGift } from '../../../models/db-gift/creat-gift'
import { ApplicationCommandOptionChoiceData, Interaction } from 'discord.js'
import { updateCommandOptionChoicesForGuild } from '../../../utils'
import { Language } from '../../../language'

const updateGiftToOption = async (gifts: DBGift[], interaction: Interaction, language: Language, option: string) => {
  const newChoices: ApplicationCommandOptionChoiceData[] = []
  for (const gift of gifts) {
    newChoices.push({
      name: gift.giftData.name,
      value: gift.giftData.name
    })
  }
  if (interaction.guild === null) return
  switch (option) {
    case 'create':
      await updateCommandOptionChoicesForGuild(
        interaction.guild,
        language.gift.command.name,
        language.gift.command.sendGift.name,
        language.gift.command.sendGift.stringOptionName,
        newChoices
      )
      break
    case 'remove':
      await updateCommandOptionChoicesForGuild(
        interaction.guild,
        language.gift.command.name,
        language.gift.command.removeGift.name,
        language.gift.command.removeGift.stringOptionName,
        newChoices
      )
      break
    default:
  }
}

export { updateGiftToOption }
