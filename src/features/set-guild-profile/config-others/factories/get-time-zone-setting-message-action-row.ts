import { MessageActionRow, MessageSelectMenu, MessageSelectOptionData } from 'discord.js'
import { LanguageEnum } from '../../../../models'
import moment from 'moment-timezone'
import { getLanguage } from '../../../../language'
import { timeZonesList } from './time-zones-list'

const getTimeZoneSettingMessageActionRow = (currentLanguage: LanguageEnum, currentTimeZone: string): MessageActionRow => {
  const timeZoneOptions: MessageSelectOptionData[] = []

  const language = getLanguage(currentLanguage)
  const now = moment()
  for (const timeZone of timeZonesList) {
    timeZoneOptions.push({
      label: language.setGuildProfile.otherSettingMenu.timeZoneLabel(timeZone),
      description: now.tz(timeZone).format('HH: mm'),
      value: timeZone,
      default: currentTimeZone === timeZone
    })
  }

  return new MessageActionRow()
    .addComponents([
      new MessageSelectMenu()
        .setCustomId('guildTimeZoneSettingMenu')
        .addOptions(timeZoneOptions)
    ])
}

export { getTimeZoneSettingMessageActionRow }
