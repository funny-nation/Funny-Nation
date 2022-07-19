import { Prisma } from '@prisma/client'

export type DBUser = {
    addExperience(): Promise<void>,
    resetTimeBefore(): Promise<void>
} & Prisma.UserGetPayload<Prisma.validator<Prisma.UserArgs>>
