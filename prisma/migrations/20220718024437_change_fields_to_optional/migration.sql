-- AlterTable
ALTER TABLE "Guild" ALTER COLUMN "announcementChannelID" DROP NOT NULL,
ALTER COLUMN "notificationChannelID" DROP NOT NULL,
ALTER COLUMN "administratorRoleID" DROP NOT NULL;
