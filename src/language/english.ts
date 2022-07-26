import { Language } from './index'

const english: Language = {
  errorMsg: 'Bot went wrong, please notify the server owner',
  coinBalanceDisplay (amount: number | string): string {
    return `${amount} coins`
  },
  viewProfile: {
    profile: 'Profile',
    inXXX (guildName: string): string {
      return `In ${guildName}`
    },
    yourExp: 'Your Exp'
  },
  commands: {
    getMyProfile: {
      name: 'profile',
      desc: 'View my profile'
    }
  },
  mumble: {
    mumble: 'Fxxk that guy',
    language (mumbleFrom: string, mumbleObject: string): string {
      const mubleArr = ['get out of my face', 'stfu', 'u fking asshole']
      const ramdomNumber = Math.floor(Math.random() * mubleArr.length)
      return `${mumbleFrom} speak to ${mumbleObject} that ${mubleArr[ramdomNumber]}`
    }
  },
  setGuildProfile: {
    command: 'config',
    commandDesc: 'Configure your bot in this server (Admin only)',
    title: 'Configure Your Bot',
    announcementChannelOption: 'Channel for Announcement',
    administratorRoleOption: 'Role of Administrators',
    timeZoneOption: 'Your Timezone',
    notificationChannelOption: 'Channel for Notification',
    languageOption: 'Language Setting'
  },
  transferCoin: {
    transferCommand: 'transfer',
    coin: 'coin',
    payee: 'payee',
    detail: 'remark',
    insufficientBalance: 'You have insufficient balance. ',
    transferCompleteMsg: (payeeID: string, amount: number): string => {
      return `Transfer completed! <@${payeeID}> You have received ¥${amount} coins yo。`
    },
    senderLeavingMsgInfo: 'Sender has leave a message to you. '
  }
}

export default english
