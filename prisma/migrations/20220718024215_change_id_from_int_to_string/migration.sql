-- DropForeignKey
ALTER TABLE "CoinTransfer" DROP CONSTRAINT "CoinTransfer_guildID_fkey";

-- DropForeignKey
ALTER TABLE "CoinTransfer" DROP CONSTRAINT "CoinTransfer_userID_guildID_fkey";

-- DropForeignKey
ALTER TABLE "Member" DROP CONSTRAINT "Member_guildID_fkey";

-- DropForeignKey
ALTER TABLE "Member" DROP CONSTRAINT "Member_userID_fkey";

-- AlterTable
ALTER TABLE "CoinTransfer" ALTER COLUMN "userID" SET DATA TYPE TEXT,
ALTER COLUMN "guildID" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "Guild" ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "announcementChannelID" SET DATA TYPE TEXT,
ALTER COLUMN "notificationChannelID" SET DATA TYPE TEXT,
ALTER COLUMN "administratorRoleID" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "Member" ALTER COLUMN "userID" SET DATA TYPE TEXT,
ALTER COLUMN "guildID" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "User" ALTER COLUMN "id" SET DATA TYPE TEXT;

-- AddForeignKey
ALTER TABLE "CoinTransfer" ADD CONSTRAINT "CoinTransfer_userID_guildID_fkey" FOREIGN KEY ("userID", "guildID") REFERENCES "Member"("userID", "guildID") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CoinTransfer" ADD CONSTRAINT "CoinTransfer_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Member" ADD CONSTRAINT "Member_userID_fkey" FOREIGN KEY ("userID") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Member" ADD CONSTRAINT "Member_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
