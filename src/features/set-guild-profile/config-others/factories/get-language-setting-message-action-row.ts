import { MessageActionRow, MessageSelectMenu, MessageSelectOptionData } from 'discord.js'
import { LanguageEnum } from '@prisma/client'
import { getLanguage } from '../../../../language'

const getLanguageSettingMessageActionRow = (currentLanguage: LanguageEnum): MessageActionRow => {
  const languageOptions: MessageSelectOptionData[] = []
  const language = getLanguage(currentLanguage)
  for (const lan in LanguageEnum) {
    languageOptions.push({
      label: language.setGuildProfile.otherSettingMenu.languageLabel(lan),
      description: lan,
      value: lan,
      default: currentLanguage === lan
    })
  }

  return new MessageActionRow()
    .addComponents([
      new MessageSelectMenu()
        .setCustomId('guildLanguageSettingMenu')
        .addOptions(languageOptions)
    ])
}

export { getLanguageSettingMessageActionRow }
