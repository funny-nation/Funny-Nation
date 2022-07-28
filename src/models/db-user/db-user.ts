import { User } from '@prisma/client'

export type DBUser = {
    addExperience(exp?: number): Promise<void>,
    resetTimeBefore(): Promise<void>
} & User
