import { RoleGroup } from './types/role-group'
import { Player, Tabletop } from './types/tabletop'
import {
  GuildMember,
  MessageActionRow,
  MessageButton,
  TextBasedChannel
} from 'discord.js'
import { getProcessControlActionRow } from './get-process-control-action-row'
import { getLanguage, Language } from '../../../language'
import { sendMsgThenDelete } from '../../../utils'
import { getDbGuild } from '../../../models'

const tabletops = new Map<string, Tabletop>()
const timeoutInMS = 1200000

setInterval(async () => {
  const now = new Date()
  for (const [, tableTop] of tabletops) {
    const guild = tableTop.owner.guild
    const dbGuild = await getDbGuild(guild.id)
    const language = getLanguage(dbGuild.languageInGuild)
    if (now.getTime() - tableTop.lastActiveTime.getTime() > timeoutInMS) {
      tableTop.destroy()
      sendMsgThenDelete(tableTop.channel, language.tabletopRoleAssign.longTimeNoActiveError)
    }
  }
}, 300000)

const newTabletop = (channel: TextBasedChannel, roleGroups: RoleGroup[], owner: GuildMember, maxNumberPlayer: number, language: Language): Tabletop | null => {
  if (tabletops.has(channel.id)) {
    return null
  }
  tabletops.set(channel.id, {
    lastActiveTime: new Date(),
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
      this.resetLastActiveTime()
      return true
    },
    addPlayerToBlacklist (memberId: string): boolean {
      if (this.blacklists.indexOf(memberId) !== -1) return false
      this.blacklists.push(memberId)
      this.resetLastActiveTime()
      return true
    },
    dropPlayer (memberID: string): boolean {
      if (!this.players.has(memberID)) return false
      this.players.delete(memberID)
      this.resetLastActiveTime()
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
      this.resetLastActiveTime()
      return components
    },
    resetLastActiveTime () {
      this.lastActiveTime = new Date()
    }
  })
  return tabletops.get(channel.id) || null
}

const getTabletop = (channelID: string): Tabletop | null => {
  const result = tabletops.get(channelID)
  return result || null
}

export { newTabletop, getTabletop }
