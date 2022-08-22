import { InventoryCategory, Inventory } from '@prisma/client'
import { prismaClient } from '../../prisma-client'
import { getDbUser } from '../db-user'

const createInventory = async (name: string, inventoryValue: number, category: InventoryCategory, ownerID: string, createdAt: Date, guildID: string): Promise<Inventory> => {
  await getDbUser(ownerID)
  return await prismaClient.inventory.create({
    data: {
      name,
      inventoryValue,
      category,
      ownerID,
      createdAt,
      guildID
    }
  })
}

export { createInventory }
