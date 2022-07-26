import { Member } from '@prisma/client'

export type DBMember = {
    addMemberExperience(exp?: number): Promise<void>,
    addCoins(coins?: number): Promise<void>,
    reduceCoins(coins?: number): Promise<void>
} & Member
