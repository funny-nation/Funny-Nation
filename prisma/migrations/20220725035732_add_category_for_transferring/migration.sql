-- CreateEnum
CREATE TYPE "TransferCategory" AS ENUM ('transferIn', 'transferOut', 'issueCoin');

-- AlterTable
ALTER TABLE "CoinTransfer" ADD COLUMN     "category" "TransferCategory" NOT NULL DEFAULT 'issueCoin';
