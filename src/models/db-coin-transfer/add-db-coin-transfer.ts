import { prismaClient } from '../../prisma-client'
import moment from 'moment-timezone'
import { DbCoinTransfer } from './db-coin-transfer'
import { TransferCategory } from '../enum'
import { randomUUID } from 'crypto'

const addDbCoinTransfer = async (userID: string, guildID: string, amount: number, transactionID: string | null, detail: string, category?: TransferCategory): Promise<DbCoinTransfer> => {
  if (!transactionID) {
    transactionID = randomUUID()
  }
  return await prismaClient.coinTransfer.create({
    data: {
      userID,
      guildID,
      amount,
      transactionID,
      time: moment().utc().toDate(),
      detail,
      category
    }
  })
}

export { addDbCoinTransfer }
