import { LanguageEnum } from '../models'
import { Gift } from '../features/gift/gift-type'
import { CoinTransfer } from '@prisma/client'
import { EmbedFieldData, User } from 'discord.js'

export interface Language {
    errorMsg: string,
    coinBalanceDisplay(amount: number | string, ranking: number): string,
    viewProfile: {
        profile: string,
        expInThisGuild(guildName: string, ranking: number): string,
        expInThisBot(ranking: number): string
    }
    commands: {
        getMyProfile: {
            name: string,
            desc: string
        }
    },
    curse: {
        curse: string,
        language: string[]
    },
    setGuildProfile: {
        commands: {
            name: string,
            desc: string,
            subcommand: {
                setAdmin: {
                    name: string,
                    desc: string,
                    optionName: string,
                    optionDesc: string
                },
                setAnnouncement: {
                    name: string,
                    desc: string,
                    optionName: string,
                    optionDesc: string
                },
                setNotificationChannel: {
                    name: string,
                    desc: string,
                    optionName: string,
                    optionDesc: string
                },
                setOthers: {
                    name: string,
                    desc: string,
                }
            }
        },
        invalidAccess: string,
        successMsg: {
            setLanguage(language: LanguageEnum): string,
            setAdminRole(roleName: string): string,
            setNotificationChannel(channelName: string): string,
            setAnnouncementChannel(channelName: string): string,
            setTimeZone(timeZoneName: string): string
        },
        languageUpdateSoFrequent: string,
        otherSettingMenu: {
            title: string,
            languageLabel(language: string): string,
            timeZoneLabel(timeZone: string): string
        },
        close: string
    },
    transferCoin: {
        transferCommand: string,
        commandDesc: string,
        commandLang: string,
        coin: string,
        coinDesc: string,
        amountDesc: string,
        payee: string,
        payeeDesc: string,
        detail: string,
        detailDesc: string,
        insufficientBalance: string,
        transferCompleteMsg(payeeID: string, amount: number): string,
        senderLeavingMsgInfo: string
        integerOnly: string,
        invalidInt: string,
        transactionFailed: string
    },
    addCoinsExpToUserInVoice: {
        coinTransferMsg(coins: number, totalMinutes: number): string
    },
    anonymousMsg: {
        commands: {
            desc: string,
            setName: {
                name: string,
                desc: string,
                optionName: string
            },
            send: {
                name: string,
                desc: string,
                MsgOptionName: string,
                UserOptionName: string
            }
        },
        yourNewNameIs: string
    },
    leaderBoard: {
        command: {
            name: string,
            desc: string
        },
        coinsLeaderBoard: string,
        expLeaderBoard: string,
        coinsDisplay(coins: number): string
    },
    gift: {
        errorHandler:{
            botReply: string,
            userReply: string
        }
        command: {
            name: string,
            desc: string,
            subCommand: {
                name: string,
                desc: string,
                stringOptionName: string,
                stringOptionDesc: string,
                userOptionName: string,
                userOptionDesc: string
            }
        },
        embedTitle: string,
        embedDesc: string
        hasEnoughMoney: string,
        presetGifts: {
            gift1: Gift,
            gift2: Gift
        }
    },
    dailyCheckIn: {
        titleForBooster: string,
        desc(money: number): string
    },
    transactionsHistory: {
        commandName: string,
        transactionHistoryTitle: string,
        fieldEntry(transaction: CoinTransfer, tz: string): EmbedFieldData,
        commandDesc: string
    },
    transferCategories: {
        transferIn: string,
        transferOut: string,
        issueCoin: string,
        collectCoin: string,
        earnFromVoice: string,
        earnFromMessage: string,
        earnFromCheckIn: string,
        sendGift: string
    }
    notification: string,
    tabletopRoleAssign:{
        cannotCloseGame: string,
        oneTypeRoleError: string,
        fullOfPeople: string,
        kickOutByOwner: string,
        kickOutError: string,
        onlyOwnerCanStart: string,
        notEnoughPeople: string,
        endTabletop: string,
        tabletopTitle: string,
        tabletopDescription: string,
        tabletopClose: string,
        joinTabletop: string,
        tabletopStart: string
        leaveTabletop: string,
        channelUsed: string
        commandsDescription:string,
        subcommandDescription: string,
        subcommandName: string
    }
}
