import { Member } from '@prisma/client'
import { prismaClient } from '../../prisma-client'

type LeaderBoard = {
  exp: Member[],
  coins: Member[]
}

const getLeaderBoard = async (guildID: string): Promise<LeaderBoard> => {
  const exp = await prismaClient.member.findMany({
    take: 5,
    where: {
      guildID
    },
    orderBy: [{
      experienceInGuild: 'desc'
    }]
  })
  const coins = await prismaClient.member.findMany({
    take: 5,
    where: {
      guildID
    },
    orderBy: [{
      coinBalanceInGuild: 'desc'
    }]
  })
  return {
    exp,
    coins
  }
}

export { getLeaderBoard, LeaderBoard }
