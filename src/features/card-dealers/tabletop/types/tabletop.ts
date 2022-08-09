import { TextBasedChannel, GuildMember, MessageActionRow } from 'discord.js'
import { Card } from './card'

export type Player = {
  member: GuildMember,
  messageActionRow: MessageActionRow
}

export type Tabletop = {
  channel: TextBasedChannel,
  cards: Card[],
  players: Map<string, Player>,
  owner: GuildMember,
  blacklists: string[],
  maxNumberPlayer: number,
  destroy(): void,
  addPlayer(member: GuildMember): boolean,
  dropPlayer(memberID: string): boolean,
  renderComponents(): MessageActionRow[],
  addPlayerToBlacklist (memberId: string): boolean
}
