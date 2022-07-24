import { MessageActionRow, MessageSelectMenu, MessageSelectOptionData } from 'discord.js'
import LanguageEnum from '../../../../models/LanguageEnum'
const getLanguageSettingMessageActionRow = (currentLanguage: LanguageEnum): MessageActionRow => {
  const languageOptions: MessageSelectOptionData[] = []

  for (const lan in LanguageEnum) {
    languageOptions.push({
      label: `Language: ${lan}`,
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

export default getLanguageSettingMessageActionRow
