import { User } from 'discord.js'

type gift = {
  name: string,
  pictureURL: string,
  desc: string,
  price: number,
  announcement(sender: User, receiver: User): string
}

const giftInfo = new Map<string, gift>()

giftInfo.set('001', {
  name: 'Gift 1',
  pictureURL: '123',
  desc: 'qwe',
  price: 1,
  announcement (sender: User, receiver: User): string {
    return `${sender} send Gift 1 to ${receiver}`
  }
})

export { giftInfo }
