import { addDbCoinTransfer, getDbMember } from '../../models'
import { randomUUID } from 'crypto'
import { logger } from '../../logger'
import { TransactionStatus } from './transaction-status'

async function coinTransferHelper (payerID: string, payeeID: string, guildID: string, amount: number, detail?: string | null): Promise<TransactionStatus> {
  logger.info(`payerID: ${payeeID} made a transfer to payeeID: ${payeeID} of ${amount} coins. Detail msg: ${detail}`)
  const payerDbMember = await getDbMember(payerID, guildID)
  const payeeDbMember = await getDbMember(payeeID, guildID)

  if (amount > payerDbMember.coinBalanceInGuild) {
    logger.info('This transaction failed because of payer\'s insufficient balance')
    return TransactionStatus.INSUFFICIENT_BALANCE
  }
  if (amount < 1) {
    logger.info(`transaction failed because amount < 1: ${amount}`)
    return TransactionStatus.FAILED
  }
  await payerDbMember.reduceCoins(amount)
  logger.info(`coins from payer: ${payerID} have been deducted successfully`)
  await payeeDbMember.addCoins(amount)
  logger.info(`coins added to payee: ${payeeID} successfully`)
  const transactionID = randomUUID()
  await addDbCoinTransfer(payeeID, guildID, amount, transactionID, detail || '', 'transferOut')
  await addDbCoinTransfer(payerID, guildID, -amount, transactionID, detail || '', 'transferIn')
  logger.info(`transaction records have been updated to database successfully. ID: ${transactionID}`)
  return TransactionStatus.SUCCESS
}

export { coinTransferHelper }
