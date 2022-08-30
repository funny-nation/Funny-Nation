/*
  Warnings:

  - You are about to drop the column `createTime` on the `Inventory` table. All the data in the column will be lost.
  - You are about to drop the column `sourceID` on the `Inventory` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Inventory" DROP COLUMN "createTime",
DROP COLUMN "sourceID",
ADD COLUMN     "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "inventoryValue" BIGINT NOT NULL DEFAULT 0;

-- CreateTable
CREATE TABLE "Gift" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "emoji" TEXT NOT NULL,
    "price" BIGINT NOT NULL,
    "giftAnnouncement" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "guildID" TEXT NOT NULL,

    CONSTRAINT "Gift_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Inventory" ADD CONSTRAINT "Inventory_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Gift" ADD CONSTRAINT "Gift_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
