import { Language } from './index'
import { LanguageEnum } from '../models'
import { User } from 'discord.js'
import moment from 'moment-timezone'

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
  coinBalanceDisplay (amount: number | string, ranking: number): string {
    return `你有${amount}金币 • 目前排名：#${ranking}`
  },
  viewProfile: {
    profile: '档案',
    expInThisGuild (guildName: string, ranking: number): string {
      return `在${guildName}，你排名#${ranking}`
    },
    expInThisBot (ranking: number): string {
      return `在这个世界，你排名#${ranking}`
    }
  },
  commands: {
    getMyProfile: {
      name: 'profile',
      desc: '查看我的信息'
    }
  },
  curse: {
    curse: '嘲讽ta',
    language: [
      '百度搜不到你，搜狗一定能搜到。',
      '你长个脑子就是为了凑身高蛮！',
      '听君一席话，白读十年书。',
      '你这嘴腌了几年啊这么入味儿。',
      '你的链子只在关键时候掉。',
      '你说得有点道理，也不至于一点道理也没有。',
      '就这就这就这就这？',
      '急了急了急了急了？',
      '不会吧不会吧不会有人急了吧？',
      '等我有钱了，我就带我你去最好的神经医院。',
      '你在人群中渺小，在猪圈里伟大！',
      '一巴掌把你乎墙上扣都扣不下来。',
      '你的样子好棒哦，跟棒槌一个样',
      '也许你自己的无能使你这么没有自信。',
      '作为失败的典型，你实在是太成功了。',
      '真不好意思，让您贱笑了。'
    ]
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
    coinDesc: '金币转账',
    amountDesc: '金币数额',
    detailDesc: '给收款人的转账备注',
    payeeDesc: '在本Guild中的收款人账号',
    invalidInt: '请在金额框内输入数字',
    integerOnly: '请输入数字',
    transactionFailed: '转账失败，可能是由于服务器内部错误。'
  },
  addCoinsExpToUserInVoice: {
    coinTransferMsg (coins: number, totalMinutes: number) {
      return `你在语音频道呆了${totalMinutes}分钟赚了${coins}金币`
    }
  },
  notification: '一个来自异次元的通知',
  anonymousMsg: {
    commands: {
      desc: '匿名消息',
      setName: {
        name: '设置昵称',
        desc: '设置你的匿名消息的昵称',
        optionName: '昵称'
      },
      send: {
        name: '发送',
        desc: '发送匿名消息',
        MsgOptionName: '消息',
        UserOptionName: '提到谁'
      }
    },
    yourNewNameIs: '你的新昵称是：'
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
  },
  dailyCheckIn: {
    titleForBooster: '你好呀Booster，今日签到成功',
    desc (money: number): string {
      return `你获得了${money}金币`
    }
  },
  transactionsHistory: {
    commandName: 'transactions',
    transactionHistoryTitle: '金币交易历史',
    commandDesc: '近10笔金币交易记录',
    fieldEntry ({ amount, category, detail, time }, tz) {
      return {
        name: `于${moment(time).tz(tz).format('MM月DD日 HH:MM')}${amount > 0 ? `收到${amount}` : `失去${-amount}`}个金币`,
        value: `交易属于${chineseSimplified.transferCategories[category]}${detail ? '，' : ''}${detail}`,
        inline: false
      }
    }
  },
  transferCategories: {
    transferIn: '转入金币',
    transferOut: '转出金币',
    issueCoin: '放水',
    collectCoin: '收税',
    earnFromVoice: '语音收入',
    earnFromMessage: '消息收入',
    earnFromCheckIn: '签到收入',
    sendGift: '送礼',
    buyBadge: '购买徽章'
  },
  tabletopRoleAssign: {
    cannotCloseGame: ' 你不是该游戏拥有者，无法关闭此次游戏',
    oneTypeRoleError: '只设置一个类型的身份玩不起来啊',
    fullOfPeople: ' 这局人满了，等下一局吧！',
    kickOutByOwner: ' 您已被踢出，无法再次进入',
    kickOutError: ' 您不是房主，无法将别人移除',
    onlyOwnerCanStart: '只有房主可以开始游戏',
    notEnoughPeople: '这局人还没满，再等等吧！',
    endTabletop: '发牌结束，祝您玩得开心',
    tabletopTitle: '来自',
    tabletopDescription: '的发牌器',
    tabletopClose: '关闭',
    joinTabletop: '加入',
    tabletopStart: '发牌',
    leaveTabletop: '踢ta/离开',
    channelUsed: '该频道已被占用',
    subcommandDescription: '可定制角色内容和玩家数量的发牌器，每个玩家一个角色',
    commandsDescription: '发牌器',
    subcommandName: '自定义角色'
  },
  monetaryControl: {
    coinCommand: 'coin',
    coinDesc: 'coinDesc',
    issueSubcommand: '放水',
    issueDesc: '给指定用户增加指定数量的金币',
    collectSubcommand: '收税',
    collectDesc: '从指定用户的账户中扣去指定数量的金币',
    amountOption: '金额',
    amountDesc: '指定金币的数量',
    targetUserOption: '用户',
    targetUserDesc: '被馅饼砸中的用户',
    notAdministratorMsg: '你不是管理员。',
    collectedSuccessInfo (targetUser, amount: number): string {
      return `${targetUser}自愿上交了${amount}个金币。感谢TA为社区做出的贡献。`
    },
    issuedSuccessInfo (targetUser, amount: number): string {
      return `群主大发慈悲，随手给${targetUser}施舍了${amount}个金币。`
    }
  },
  randomNumber: {
    subcommandName: '随机数',
    subcommandDescription: '为您生成对应设置的随机数',
    firstNumberOptionName: '第一个数',
    secondNumberOptionName: '第二个数',
    rangeNumberOptionName: '生成个数',
    firstNumberOptionDescription: '随机数最小值',
    secondNumberOptionDescription: '随机数最大值',
    rangeNumberOptionDescription: '随机数生成个数',
    embedMessageTitle: '您生成的随机数是：',
    minNumberIsMaxNumberError: '错误：您的第一个数和第二个数不能一样'
  }
}

export default chineseSimplified
