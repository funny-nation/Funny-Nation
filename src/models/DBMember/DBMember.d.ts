import { Prisma } from '@prisma/client'

export type DBMember = {
    addMemberExperience(): Promise<void>,
    addCoins(): Promise<void>
} & Prisma.MemberGetPayload<Prisma.validator<Prisma.MemberArgs>>
