import { addDbCoinTransfer, getDbMember } from '../../models'

const collectCoinsFromUser = async (guildID: string, userID: string, amount: number) => {
  const member = await getDbMember(userID, guildID)
  const balance = await member.coinBalanceInGuild
  if ((balance - BigInt(amount)) < 0) {
    amount = Number(balance)
  }
  await member.reduceCoins(amount)
  await addDbCoinTransfer(userID, guildID, -amount, null, '', 'collectCoin')
}

const issueCoinsToUser = async (guildID: string, userID: string, amount: number) => {
  await (await getDbMember(userID, guildID)).addCoins(amount)
  await addDbCoinTransfer(userID, guildID, amount, null, '', 'issueCoin')
}

export { collectCoinsFromUser, issueCoinsToUser }
