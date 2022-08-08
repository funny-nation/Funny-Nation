import { InventoryCategory, Inventory } from '@prisma/client'
import { prismaClient } from '../../prisma-client'

const createInventory = async (name: string, category: InventoryCategory, sourceID: string, ownerID: string): Promise<Inventory> => {
  return await prismaClient.inventory.create({
    data: {
      name,
      category,
      sourceID,
      ownerID
    }
  })
}

export { createInventory }
