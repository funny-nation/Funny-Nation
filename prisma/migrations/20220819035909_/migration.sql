/*
  Warnings:

  - The primary key for the `Gift` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `Gift` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[name,guildID]` on the table `Gift` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "Gift" DROP CONSTRAINT "Gift_pkey",
DROP COLUMN "id";

-- CreateIndex
CREATE UNIQUE INDEX "Gift_name_guildID_key" ON "Gift"("name", "guildID");
