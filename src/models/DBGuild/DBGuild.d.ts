import { Prisma } from '@prisma/client'

export type DBGuild = Prisma.GuildGetPayload<Prisma.validator<Prisma.GuildArgs>>
