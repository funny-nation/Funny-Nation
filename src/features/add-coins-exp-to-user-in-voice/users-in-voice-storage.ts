import moment from 'moment-timezone'
import { logger } from '../../logger'

const storage = new Map<string, Date>()

setInterval(() => {
  logger.info(`Currently, there are ${storage.size} users in voice channel`)
}, 60000)

/**
 * Attach user to UIV storage by user id
 * @param userID
 */
const attachUserToUIVStorage = (userID: string) => {
  const now = moment().utc().toDate()
  storage.set(userID, now)
}

/**
 * Detach user from UIV storage by user id, and return the total minute
 * @param userID
 */
const detachUserFromUIVStorage = (userID: string): number => {
  const now = moment().utc().toDate()
  const timeWhenUserJoinChannel = storage.get(userID)
  storage.delete(userID)
  if (!timeWhenUserJoinChannel) return 0
  const deltaTimeInMS = now.getTime() - timeWhenUserJoinChannel.getTime()
  const deltaTimeInMinute = deltaTimeInMS / 60000
  if (deltaTimeInMinute < 1) return 0
  return Math.round(deltaTimeInMinute)
}

export { attachUserToUIVStorage, detachUserFromUIVStorage }
