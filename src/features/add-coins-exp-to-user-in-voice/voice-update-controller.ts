import { client } from '../../client'
import { VoiceState } from 'discord.js'
import { attachUserToUIVStorage } from './users-in-voice-storage'
import { logger } from '../../logger'
import { coinExpAdder } from './coin-exp-adder'

client.on('voiceStateUpdate', async (oldVoiceState: VoiceState, newVoiceState: VoiceState) => {
  try {
    if (oldVoiceState.channelId === null && newVoiceState.channelId !== null && newVoiceState.member !== null) {
      logger.verbose(`User "${newVoiceState.member.displayName}" joins the voice channel`)
      attachUserToUIVStorage(newVoiceState.id)
      return
    }
    if (oldVoiceState.channelId !== null && newVoiceState.channelId === null) {
      await coinExpAdder(oldVoiceState)
      return
    }
    if (oldVoiceState.channelId !== null && newVoiceState.channelId !== oldVoiceState.channelId && newVoiceState.member !== null) {
      await coinExpAdder(oldVoiceState)
      attachUserToUIVStorage(newVoiceState.id)
      logger.verbose(`User "${newVoiceState.member.displayName}" joins the voice channel`)
      return
    }
  } catch (e) {
    console.log(e)
    logger.error('Error occur when adding coins and exp to user in voice')
  }
})
