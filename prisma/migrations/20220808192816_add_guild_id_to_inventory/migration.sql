/*
  Warnings:

  - Added the required column `guildID` to the `Inventory` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Inventory" ADD COLUMN     "guildID" TEXT NOT NULL;
