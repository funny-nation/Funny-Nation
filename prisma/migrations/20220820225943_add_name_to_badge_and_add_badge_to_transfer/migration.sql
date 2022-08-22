/*
  Warnings:

  - Added the required column `name` to the `Badge` table without a default value. This is not possible if the table is not empty.

*/
-- AlterEnum
ALTER TYPE "TransferCategory" ADD VALUE 'buyBadge';

-- AlterTable
ALTER TABLE "Badge" ADD COLUMN     "name" TEXT NOT NULL;
