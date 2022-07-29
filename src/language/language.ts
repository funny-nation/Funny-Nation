import { LanguageEnum } from '../models'

export interface Language {
    errorMsg: string,
    coinBalanceDisplay(amount: number | string): string,
    viewProfile: {
        profile: string,
        inXXX(guildName: string): string,
        yourExp: string
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
        invalidInt: string
    },
    addCoinsExpToUserInVoice: {
        coinTransferMsg(coins: number, totalMinutes: number): string
    }
}
