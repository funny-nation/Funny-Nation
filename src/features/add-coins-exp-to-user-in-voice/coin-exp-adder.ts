import { detachUserFromUIVStorage } from './users-in-voice-storage'
import { logger } from '../../logger'
import { addDbCoinTransfer, getDbGuild, getDbMember, getDbUser } from '../../models'
import { getLanguage } from '../../language'
import { VoiceState } from 'discord.js'

const coinExpAdder = async (oldVoiceState: VoiceState) => {
  const userID = oldVoiceState.id
  const totalMinute = detachUserFromUIVStorage(userID)
  if (oldVoiceState.member === null) return

  if (totalMinute === 0) {
    logger.verbose(`User "${oldVoiceState.member.displayName}" lefts the voice channel and earn nothing`)
    return
  }

  const dbMember = await getDbMember(userID, oldVoiceState.guild.id)
  const dbUser = await getDbUser(userID)
  const dbGuild = await getDbGuild(oldVoiceState.guild.id)

  const coinsAdd = totalMinute
  const expAdd = totalMinute

  const language = getLanguage(dbGuild.languageInGuild)
  await dbMember.addMemberExperience(expAdd)
  await addDbCoinTransfer(
    userID, oldVoiceState.guild.id,
    totalMinute,
    null,
    language.addCoinsExpToUserInVoice.coinTransferMsg(coinsAdd, expAdd),
    'earnFromVoice'
  )
  await dbMember.addCoins(coinsAdd)
  await dbUser.addExperience(expAdd)
  logger.verbose(`User "${oldVoiceState.member.displayName}" lefts the voice channel. He/She earn ${coinsAdd} coins by staying for ${totalMinute} minutes`)
}
export { coinExpAdder }
