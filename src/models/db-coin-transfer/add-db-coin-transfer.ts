import prismaClient from '../../prismaClient'
import moment from 'moment-timezone'
import { DbCoinTransfer } from './db-coin-transfer'
import { TransferCategory } from '../enum/TransferCategory'

const addDbCoinTransfer = async (userID: string, guildID: string, amount: number, transactionID: string, detail: string, category?: TransferCategory): Promise<DbCoinTransfer> => {
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

export default addDbCoinTransfer