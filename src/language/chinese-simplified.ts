import { Language } from './index'
import { LanguageEnum } from '../models'

const chineseSimplified: Language = {
  errorMsg: 'Bot莫名其妙炸了，麻烦通知一下群主',
  coinBalanceDisplay (amount: number | string): string {
    return `金币：${amount}`
  },
  viewProfile: {
    profile: '档案',
    inXXX (guildName: string): string {
      return `在${guildName}`
    },
    yourExp: '你自己的'
  },
  commands: {
    getMyProfile: {
      name: 'profile',
      desc: '查看我的信息'
    }
  },
  mumble: {
    mumble: '骂ta',
    language (mumbleFrom: string, mumbleObject: string): string {
      const mubleArr = ['草泥马', '我去年买了个表', '你tm的', '你是不是傻']
      const ramdomNumber = Math.floor(Math.random() * mubleArr.length)
      return `${mumbleFrom}对${mumbleObject}说："${mubleArr[ramdomNumber]}"`
    }
  },
  setGuildProfile: {
    commands: {
      name: 'config',
      desc: '设置这个Bot',
      subcommand: {
        setAdmin: {
          name: '管理员',
          desc: '设置管理员Tag',
          optionName: 'tag',
          optionDesc: '管理员的Tag'
        },
        setAnnouncement: {
          name: '公告栏',
          desc: '设置公告文字频道',
          optionName: '频道',
          optionDesc: '公告文字频道'
        },
        setNotificationChannel: {
          name: '通知栏',
          desc: '设置通知文字频道',
          optionName: '频道',
          optionDesc: '通知文字频道'
        },
        setOthers: {
          name: '其他',
          desc: '设置语言与时区'
        }
      }
    },
    invalidAccess: '无权访问',
    successMsg: {
      setLanguage (language: LanguageEnum) {
        return `语言设置成功，你现在的语言是"${language}"`
      },
      setAdminRole (roleName: string) {
        return `管理员设置成功，任何拥有"${roleName}"Tag的人都有Bot的管理员权限`
      },
      setNotificationChannel (channelName: string) {
        return `通知频道已设置为"${channelName}"`
      },
      setAnnouncementChannel (channelName: string) {
        return `公告频道已设置为"${channelName}"`
      },
      setTimeZone (timeZoneName: string) {
        return `时区已设置为"${timeZoneName}"`
      }
    },
    languageUpdateSoFrequent: '你需要等待一分钟后才能设置语言',
    otherSettingMenu: {
      title: '设置',
      languageLabel (language: string) {
        return `语言："${language}"`
      },
      timeZoneLabel (timeZone: string) {
        return `时区："${timeZone}"`
      }
    },
    close: '关闭'
  },
  transferCoin: {
    transferCommand: 'transfer',
    commandLang: '转账',
    coin: '金币',
    payee: '收款人',
    detail: '备注',
    insufficientBalance: '金币不足',
    transferCompleteMsg: (payeeID: string, amount: number): string => {
      return `转账成功 <@${payeeID}> 你发达了。刚收到了¥${amount}个金币哟。`
    },
    senderLeavingMsgInfo: '转账人给你留了一条信息。',
    commandDesc: '给Guild里的其他用户转账',
    coinDesc: '金币',
    amountDesc: '金币数额',
    detailDesc: '给收款人的转账备注',
    payeeDesc: '在本Guild中的收款人账号'
  }
}

export default chineseSimplified
