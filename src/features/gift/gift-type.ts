import { User } from 'discord.js'

export type Gift = {
  name: string,
  pictureURL: string,
  desc: string,
  price: number,
  announcement(sender: User, receiver: User): string
}
