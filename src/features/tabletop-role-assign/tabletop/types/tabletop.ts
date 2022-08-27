import { TextBasedChannel, GuildMember, MessageActionRow } from 'discord.js'
import { RoleGroup } from './role-group'
import { Language } from '../../../../language'

export type Player = {
  member: GuildMember,
  messageActionRow: MessageActionRow
}

export type Tabletop = {
  lastActiveTime: Date
  channel: TextBasedChannel,
  roleGroups: RoleGroup[],
  players: Map<string, Player>,
  owner: GuildMember,
  blacklists: string[],
  maxNumberPlayer: number,
  language: Language,
  destroy(): void,
  addPlayer(member: GuildMember): boolean,
  dropPlayer(memberID: string): boolean,
  renderComponents(): MessageActionRow[],
  addPlayerToBlacklist (memberId: string): boolean,
  resetLastActiveTime(): void
}
