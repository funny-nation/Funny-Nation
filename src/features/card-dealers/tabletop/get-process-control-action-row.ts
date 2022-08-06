import { MessageButton, MessageActionRow } from 'discord.js'

const getProcessControlActionRow = () => {
  return new MessageActionRow()
    .addComponents([
      new MessageButton()
        .setLabel('发牌')
        .setCustomId('cardDealerStartButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel('关闭')
        .setCustomId('cardDealerCloseButton')
        .setStyle('SECONDARY'),
      new MessageButton()
        .setLabel('加入')
        .setCustomId('cardDealerJoinButton')
        .setStyle('PRIMARY')
    ])
}

export { getProcessControlActionRow }
