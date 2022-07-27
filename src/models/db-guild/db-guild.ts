import { Guild } from '@prisma/client'
import { LanguageEnum } from '../enum'

export type DBGuild = {
  setAnnouncementChannelID(announcementChannelID: string): Promise<void>,
  setLanguageInGuild(languageInGuild: LanguageEnum): Promise<void>,
  setNotificationChannelID(notificationChannelID: string): Promise<void>,
  setAdministratorRoleID(administratorRoleID: string): Promise<void>,
  setTimeZone(timeZone: string): Promise<void>,
  resetCommandsUpdatedAt(): Promise<void>
} & Guild
