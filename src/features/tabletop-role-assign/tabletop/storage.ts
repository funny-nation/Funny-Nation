import { RoleGroup } from './types/role-group'
import { Player, Tabletop } from './types/tabletop'
import { GuildMember, MessageActionRow, MessageButton, TextBasedChannel } from 'discord.js'
import { getProcessControlActionRow } from './get-process-control-action-row'
import { Language } from '../../../language'

const tabletops = new Map<string, Tabletop>()

const newTabletop = (channel: TextBasedChannel, roleGroups: RoleGroup[], owner: GuildMember, maxNumberPlayer: number, language: Language): Tabletop | null => {
  if (tabletops.has(channel.id)) {
    return null
  }
  tabletops.set(channel.id, {
    blacklists: [],
    channel,
    roleGroups,
    players: new Map<string, Player>(),
    owner,
    maxNumberPlayer,
    language,
    addPlayer (member: GuildMember): boolean {
      if (this.players.has(member.id)) return false
      this.players.set(member.id, {
        member,
        messageActionRow: new MessageActionRow()
          .addComponents([
            new MessageButton()
              .setLabel(member.displayName)
              .setCustomId(member.id)
              .setStyle('SUCCESS')
              .setDisabled(true),
            new MessageButton()
              .setLabel(language.tabletopRoleAssign.leaveTabletop)
              .setStyle('SUCCESS')
              .setCustomId('tabletopKickPlayerButton' + member.id)
          ])
      })
      return true
    },
    addPlayerToBlacklist (memberId: string): boolean {
      if (this.blacklists.indexOf(memberId) !== -1) return false
      this.blacklists.push(memberId)
      return true
    },
    dropPlayer (memberID: string): boolean {
      if (!this.players.has(memberID)) return false
      this.players.delete(memberID)
      return true
    },
    destroy () {
      tabletops.delete(this.channel.id)
    },
    renderComponents (): MessageActionRow[] {
      const components: MessageActionRow[] = [getProcessControlActionRow(language)]
      for (const [, player] of this.players) {
        components.push(player.messageActionRow)
      }
      return components
    }
  })
  return tabletops.get(channel.id) || null
}

const getTabletop = (channelID: string): Tabletop | null => {
  const result = tabletops.get(channelID)
  return result || null
}

export { newTabletop, getTabletop }
