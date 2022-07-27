/*
  Warnings:

  - You are about to drop the column `languageUpdatedAt` on the `Guild` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "Guild" DROP COLUMN "languageUpdatedAt",
ADD COLUMN     "commandsUpdatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;
