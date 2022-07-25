import { MessageActionRow, MessageSelectMenu, MessageSelectOptionData } from 'discord.js'
import { LanguageEnum } from '../../../../models/enum/language-enum'
import moment from 'moment-timezone'

const timeZones = [
  'America/Los_Angeles',
  'America/New_York',
  'America/Chicago',
  'America/Denver',
  'Asia/Shanghai',
  'Australia/Sydney',
  'Europe/London'
]

const getTimeZoneSettingMessageActionRow = (currentLanguage: LanguageEnum, currentTimeZone: string): MessageActionRow => {
  const timeZoneOptions: MessageSelectOptionData[] = []

  const now = moment()
  for (const timeZone of timeZones) {
    timeZoneOptions.push({
      label: `Time Zone: ${timeZone}`,
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

export default getTimeZoneSettingMessageActionRow
