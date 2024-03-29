import { User } from '@prisma/client'

export type DBUser = {
    addExperience(exp?: number): Promise<void>,
    resetTimeBefore(): Promise<void>,
    setAnonymousNickName(anonymousNickName: string): Promise<void>,
    getExpRanking(): Promise<number>
} & User
