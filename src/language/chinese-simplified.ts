import { Language } from './index'
import { LanguageEnum } from '../models'
import { User } from 'discord.js'

const chineseSimplified: Language = {
  leaderBoard: {
    coinsDisplay: function (coins: number) {
      return `¥ ${coins}`
    },
    coinsLeaderBoard: '金币排行榜',
    command: {
      desc: '排行榜查看',
      name: 'leaderboard'
    },
    expLeaderBoard: '等级排行榜'
  },
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
  curse: {
    curse: '嘲讽ta',
    language: ['就这？', '你是不是傻', 'SB', '你大爷的']
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
      return `转账成功 \n<@${payeeID}> 你发达了。刚收到了¥${amount}个金币哟。`
    },
    senderLeavingMsgInfo: '转账人给你留了一条信息。',
    commandDesc: '给Guild里的其他用户转账',
    coinDesc: '金币',
    amountDesc: '金币数额',
    detailDesc: '给收款人的转账备注',
    payeeDesc: '在本Guild中的收款人账号',
    invalidInt: '请在金额框内输入数字',
    integerOnly: '请输入数字'
  },
  addCoinsExpToUserInVoice: {
    coinTransferMsg (coins: number, totalMinutes: number) {
      return `你在语音频道呆了${totalMinutes}分钟赚了${coins}金币`
    }
  },
  notification: '一个来自异次元的通知',
  anonymousMsg: {
    command: {
      name: 'anonymous',
      desc: '匿名消息'
    },
    sendFailed: '发送失败',
    sent: '发送成功',
    anonymousMsgFrom (nickName: string) {
      return `来自于 ${nickName} 的匿名消息`
    },
    modal: {
      title: '匿名消息',
      label: '这里输入你的匿名消息'
    }
  },
  gift: {
    errorHandler: {
      botReply: '你不能送礼物给机器人',
      userReply: '你不能送礼物给你自己'
    },
    command: {
      name: 'gift',
      desc: '一份礼物',
      subCommand: {
        name: '发送',
        desc: '发送礼物给其他人',
        stringOptionName: '发送的礼物',
        stringOptionDesc: '发送的礼物',
        userOptionName: '接收者',
        userOptionDesc: '接收者名字'
      }
    },
    embedTitle: '你收到一份新的礼物',
    embedDesc: '你收到一份新的礼物',
    hasEnoughMoney: '你太穷了',
    presetGifts: {
      gift1: {
        name: '飞机',
        pictureURL: 'https://www.funnynation.org/wp-content/uploads/2022/04/baoanduizhang.png',
        desc: '123123',
        price: 200,
        announcement (sender: User, receiver: User): string {
          return `${receiver} 收到来自老板${sender}的大飞机`
        }
      },
      gift2: {
        name: '火箭',
        pictureURL: 'https://www.funnynation.org/wp-content/uploads/2022/04/chuoqi.png',
        desc: '123123',
        price: 200,
        announcement (sender: User, receiver: User): string {
          return `${receiver} 收到来自老板${sender}的大火箭`
        }
      }
    }
  }
}

export default chineseSimplified
