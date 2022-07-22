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
    mumble: {
        mumble: string,
        language(mumbleFrom: string, mumbleObject: string): string
    }
}
