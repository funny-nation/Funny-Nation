import { Gift } from '@prisma/client'
import { prismaClient } from '../../prisma-client'

class DBGift {
  public giftData: Gift
  private constructor (gift: Gift) {
    this.giftData = gift
  }

  public static async getGift (name: string, guildID: string): Promise<DBGift | null> {
    const gift = await prismaClient.gift.findUnique({
      where: {
        name_guildID: {
          name,
          guildID
        }
      }
    })
    if (!gift) {
      return null
    }
    return new DBGift(gift)
  }

  public static async getGiftList (guildID: string): Promise<DBGift[]> {
    const giftList: Gift[] = await prismaClient.gift.findMany({
      where: {
        guildID
      }
    })
    const dbGifts: DBGift[] = []
    for (const gift of giftList) {
      dbGifts.push(new DBGift((gift)))
    }
    return dbGifts
  }

  public static async createNewGift (name: string, emoji: string, price: number, giftAnnouncement: string, description: string, guildID: string): Promise<DBGift | null> {
    const gift = await this.getGift(name, guildID)
    if (gift) {
      return null
    }
    const newGift = await prismaClient.gift.create({
      data: {
        name,
        emoji,
        price,
        giftAnnouncement,
        description,
        guildID
      }
    })
    return new DBGift(newGift)
  }

  public async remove () {
    const name = this.giftData.name
    const guildID = this.giftData.guildID
    await prismaClient.gift.delete({
      where: {
        name_guildID: {
          name,
          guildID
        }
      }
    })
  }
}

export { DBGift }
