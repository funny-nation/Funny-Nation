const guildIDs: Set<String> = new Set<String>()

const isLock = (guildID: string): boolean => guildIDs.has(guildID)

const lock = (guildID: string, msecOfLock: number = 60000) => {
  if (isLock(guildID)) return
  guildIDs.add(guildID)
  setTimeout(() => {
    guildIDs.delete(guildID)
  }, msecOfLock)
}

export const badgeUpdateLock = {
  lock,
  isLock
}
