import { Language } from '../types/Language/Language'

const englishLanguage: Language = {
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
  }
}

export default englishLanguage
