import { MessageButton, MessageActionRow } from 'discord.js'
import { Language } from '../../../language'

const getProcessControlActionRow = (language: Language) => {
  return new MessageActionRow()
    .addComponents([
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.tabletopStart)
        .setCustomId('roleAssignStartButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.tabletopClose)
        .setCustomId('roleAssignCloseButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.joinTabletop)
        .setCustomId('roleAssignJoinButton')
        .setStyle('PRIMARY')
    ])
}

export { getProcessControlActionRow }
