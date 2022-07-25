import { Member } from '@prisma/client'

export type DBMember = {
    addMemberExperience(): Promise<void>,
    addCoins(coins: number = 1): Promise<void>,
    reduceCoins(coins: number = 1): Promise<void>
} & Member
