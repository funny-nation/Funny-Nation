/*
  Warnings:

  - Added the required column `transactionID` to the `CoinTransfer` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "CoinTransfer" ADD COLUMN     "transactionID" TEXT NOT NULL;
