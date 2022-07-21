import { User } from '@prisma/client'

export type DBUser = {
    addExperience(): Promise<void>,
    resetTimeBefore(): Promise<void>
} & User
