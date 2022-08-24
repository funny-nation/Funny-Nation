import {
  ButtonInteraction,
  CommandInteraction,
  ContextMenuInteraction, InteractionReplyOptions, MessagePayload,
  ModalSubmitInteraction, SelectMenuInteraction
} from 'discord.js'
import { wait } from './wait'

type RepliableInteraction = CommandInteraction |
  ButtonInteraction |
  ContextMenuInteraction |
  SelectMenuInteraction |
  ModalSubmitInteraction

type ReplyContent = string | MessagePayload | InteractionReplyOptions

const defaultDeleteAfterMS = 20000

const replyOnlyInteractorCanSee = async (interaction: RepliableInteraction, content: ReplyContent) => {
  await interaction.deferReply({ ephemeral: true })
  await interaction.editReply(content)
}

const replyThenDelete = async (interaction: RepliableInteraction, content: ReplyContent, deleteAfterMS = defaultDeleteAfterMS) => {
  await interaction.reply(content)
  await wait(deleteAfterMS)
  await interaction.deleteReply()
}

export { replyThenDelete, replyOnlyInteractorCanSee }
