import moment from 'moment-timezone'
const timeZonesList = [
  'America/Los_Angeles',
  'America/New_York',
  'America/Chicago',
  'America/Denver',
  'Asia/Shanghai',
  'Australia/Sydney',
  'Europe/London'
]

// Timezone check
const allTimeZones = moment.tz.names()

for (const tz of timeZonesList) {
  if (!allTimeZones.includes(tz)) {
    throw new Error(`"${tz}" is not a time zone name`)
  }
}

export { timeZonesList }
