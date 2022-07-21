import { Member } from '@prisma/client'

export type DBMember = {
    addMemberExperience(): Promise<void>,
    addCoins(): Promise<void>
} & Member
