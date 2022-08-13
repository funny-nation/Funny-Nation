import { InventoryCategory, Inventory } from '@prisma/client'
import { prismaClient } from '../../prisma-client'
import { getDbUser } from '../db-user'

const createInventory = async (name: string, category: InventoryCategory, sourceID: string, ownerID: string, guildID: string): Promise<Inventory> => {
  await getDbUser(ownerID)
  return await prismaClient.inventory.create({
    data: {
      name,
      category,
      sourceID,
      ownerID,
      guildID
    }
  })
}

export { createInventory }
