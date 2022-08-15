import { DbCoinTransfer } from '../../models'
import { prismaClient } from '../../prisma-client'

const retrieveFirst10Transaction = async (userID: string, guildID: string): Promise<DbCoinTransfer[]> => {
  return await prismaClient.coinTransfer.findMany({
    take: 10,
    where: {
      userID,
      guildID
    },
    orderBy: [{
      time: 'desc'
    }]
  })
}

export { retrieveFirst10Transaction }
