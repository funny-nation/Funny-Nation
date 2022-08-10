import { MessageButton, MessageActionRow } from 'discord.js'
import { Language } from '../../../language'

const getProcessControlActionRow = (language: Language) => {
  return new MessageActionRow()
    .addComponents([
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.tabletopStart)
        .setCustomId('cardDealerStartButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.tabletopClose)
        .setCustomId('cardDealerCloseButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel(language.tabletopRoleAssign.joinTabletop)
        .setCustomId('cardDealerJoinButton')
        .setStyle('PRIMARY')
    ])
}

export { getProcessControlActionRow }
