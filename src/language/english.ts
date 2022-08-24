import { Language } from './index'
import { LanguageEnum } from '../models'
import { User } from 'discord.js'
import moment from 'moment-timezone'

const english: Language = {
  leaderBoard: {
    coinsDisplay: function (coins: number) {
      return `$ ${coins}`
    },
    coinsLeaderBoard: 'Coins Leader Board',
    command: {
      desc: 'Get leader boards',
      name: 'leaderboard'
    },
    expLeaderBoard: 'Level Lever Board'
  },
  errorMsg: 'Bot went wrong, please notify the server owner',
  coinBalanceDisplay (amount: number | string, ranking: number): string {
    return `${amount} coins • Ranking: #${ranking}`
  },
  viewProfile: {
    profile: 'Profile',
    expInThisGuild (guildName: string, ranking: number): string {
      return `In ${guildName}，your ranking: #${ranking}`
    },
    expInThisBot (ranking: number): string {
      return `In this universe, your ranking: #${ranking}`
    }
  },
  commands: {
    getMyProfile: {
      name: 'profile',
      desc: 'View my profile'
    }
  },
  curse: {
    curse: 'Curse',
    language: ['get out of my face', 'stfu', 'u fking asshole']
  },
  setGuildProfile: {
    commands: {
      name: 'config',
      desc: 'Configure this bot',
      subcommand: {
        setAdmin: {
          name: 'admin',
          desc: 'Set admin tag',
          optionName: 'tag',
          optionDesc: 'Admin tag'
        },
        setAnnouncement: {
          name: 'announcement',
          desc: 'Set the announcement channel',
          optionName: 'channel',
          optionDesc: 'Channel for announcement'
        },
        setNotificationChannel: {
          name: 'notification',
          desc: 'Set the notification channel',
          optionName: 'channel',
          optionDesc: 'Channel for notification'
        },
        setOthers: {
          name: 'others',
          desc: 'Configure language and timezone'
        }
      }
    },
    invalidAccess: 'Access denied',
    successMsg: {
      setLanguage (language: LanguageEnum) {
        return `Language has been configure to "${language}"`
      },
      setAdminRole (roleName: string) {
        return `Success, anyone with "${roleName}" tag would has admin permission`
      },
      setNotificationChannel (channelName: string) {
        return `Notification channel has been set to "${channelName}"`
      },
      setAnnouncementChannel (channelName: string) {
        return `Announcement channel has been set to "${channelName}"`
      },
      setTimeZone (timeZoneName: string) {
        return `Time zone has been set to "${timeZoneName}"`
      }
    },
    languageUpdateSoFrequent: 'You need to wait 1 minute for setting the language',
    otherSettingMenu: {
      title: 'Setting',
      languageLabel (language: string) {
        return `Language: "${language}"`
      },
      timeZoneLabel (timeZone: string) {
        return `Time zone: "${timeZone}"`
      }
    },
    close: 'Close'
  },
  transferCoin: {
    transferCommand: 'transfer',
    commandLang: 'Transfer',
    coin: 'coin',
    payee: 'payee',
    detail: 'remark',
    insufficientBalance: 'You have insufficient balance. ',
    transferCompleteMsg: (payeeID: string, amount: number): string => {
      return `Transfer completed! \n<@${payeeID}> You have received ¥${amount} coins yo。`
    },
    senderLeavingMsgInfo: 'Sender has leave a message to you. ',
    coinDesc: 'Coin',
    amountDesc: 'Coin amount',
    commandDesc: 'transfer some coins to other member in the guild',
    detailDesc: 'Remark message for the payee about this transaction',
    payeeDesc: 'The payee\'s account in this guild',
    integerOnly: 'Please enter integer only',
    invalidInt: 'Please enter an integer in the box only. ',
    transactionFailed: 'The transaction is failed due to internal error. '
  },
  addCoinsExpToUserInVoice: {
    coinTransferMsg (coins: number, totalMinutes: number) {
      return `You have earned ${coins} coins by ${totalMinutes} voice chat`
    }
  },
  notification: 'Notification',
  anonymousMsg: {
    commands: {
      desc: 'Anonymous Message',
      setName: {
        name: 'setnickname',
        desc: 'Set your nick name in anonymous message',
        optionName: 'nickname'
      },
      send: {
        name: 'send',
        desc: 'Send anonymous message',
        MsgOptionName: 'message',
        UserOptionName: 'mention'
      }
    },
    yourNewNameIs: 'Your new nick name is: '
  },
  gift: {
    errorHandler: {
      botReply: 'You cannot send gift to me',
      userReply: 'You cannot send gift to your self'
    },
    command: {
      name: 'gift',
      desc: 'a gift',
      subCommand: {
        name: 'send',
        desc: 'Send gift to others',
        stringOptionName: 'sent',
        stringOptionDesc: 'sentGift',
        userOptionName: 'receiver',
        userOptionDesc: 'receiver name'
      }
    },
    embedTitle: 'you received a new gift',
    embedDesc: 'you received a new gift',
    hasEnoughMoney: 'you poor',
    presetGifts: {
      gift1: {
        name: 'feiji',
        pictureURL: '123',
        desc: '123123',
        price: 200,
        announcement (sender: User, receiver: User): string {
          return `${receiver} received feiji from ${sender}`
        }
      },
      gift2: {
        name: 'feiji',
        pictureURL: '123',
        desc: '123123',
        price: 200,
        announcement (sender: User, receiver: User): string {
          return `${receiver} received huojian from${sender}`
        }
      }
    }
  },
  tabletopRoleAssign: {
    cannotCloseGame: ' You are not the owner of the game and cannot close this game',
    oneTypeRoleError: 'It is not possible to play with only one type of role',
    fullOfPeople: ' This game is full, wait for the next one!',
    kickOutByOwner: ' You have been kicked out by the owner and cannot re-enter',
    kickOutError: ' You are not the homeowner and cannot remove others',
    onlyOwnerCanStart: 'Only the owner can start the game',
    notEnoughPeople: 'This game is not yet full, wait a little longer.',
    endTabletop: 'The deal is over, have fun!',
    tabletopTitle: 'From',
    tabletopDescription: 'Role Dealer',
    tabletopClose: 'Close',
    joinTabletop: 'Join',
    tabletopStart: 'Deal',
    leaveTabletop: 'Kick Player/leave',
    channelUsed: 'This channel is already occupied',
    subcommandDescription: 'Dealers with customizable role contents and number of players, one role per player',
    commandsDescription: 'dealer for tabletop.ts game',
    subcommandName: 'custom-single'
  },
  dailyCheckIn: {
    titleForBooster: 'Hello dear booster, check in success',
    desc (money: number): string {
      return `You obtain ${money} coins`
    }
  },
  transactionsHistory: {
    commandName: 'transactions',
    transactionHistoryTitle: 'Coin transaction history',
    commandDesc: 'The most 10 recent coin transaction history',
    fieldEntry ({ amount, category, detail, time }, tz) {
      return {
        name: `${amount > 0 ? `${amount} coins were added` : `${-amount} coins were deducted`} at ${moment(time).tz(tz).format('HH:MM on MMM DD')}`,
        value: `${english.transferCategories[category]}${detail ? ', ' : ''}${detail}`,
        inline: false
      }
    }
  },
  transferCategories: {
    transferIn: 'Coin transfer in',
    transferOut: 'Coin transfer out',
    issueCoin: 'Issued coins by administrators',
    collectCoin: 'Collected coins by administrators',
    earnFromVoice: 'Earned coins from voice',
    earnFromMessage: 'Earned coins from sending message',
    earnFromCheckIn: 'Earned coins from checking in',
    sendGift: 'Bonus of sending gift',
    buyBadge: 'Buy Badge'
  },
  monetaryControl: {
    coinCommand: 'coin',
    coinDesc: 'coinDesc',
    issueSubcommand: 'issuingcoins',
    issueDesc: 'Issue coins to a user',
    collectSubcommand: 'collectcoins',
    collectDesc: 'Collect coins from a user',
    amountOption: 'amount',
    amountDesc: 'amount',
    targetUserOption: 'user',
    targetUserDesc: 'user',
    notAdministratorMsg: 'You are not the administrator',
    collectedSuccessInfo (targetUser, amount: number): string {
      return `Collected successfully. \n${targetUser} you lost ${amount} coins`
    },
    issuedSuccessInfo (targetUser, amount: number): string {
      return `Issued successfully. \n${targetUser} you got ${amount} coins`
    }
  },
  randomNumber: {
    subcommandName: 'random-number',
    subcommandDescription: 'Generates a random number for you that corresponds to the setting',
    firstNumberOptionName: 'the-first-number',
    secondNumberOptionName: 'the-second-number',
    rangeNumberOptionName: 'number-of-generated',
    firstNumberOptionDescription: 'Random number minimum',
    secondNumberOptionDescription: 'Random number maximum',
    rangeNumberOptionDescription: 'Number of random numbers generated',
    embedMessageTitle: 'The random number you generate is：',
    minNumberIsMaxNumberError: 'Error: Your first number and second number cannot be the same'
  }
}

export default english
