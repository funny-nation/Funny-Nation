-- CreateTable
CREATE TABLE "User" (
    "id" BIGINT NOT NULL,
    "timeBefore" TIMESTAMP(3) NOT NULL,
    "experiece" BIGINT NOT NULL
);

-- CreateTable
CREATE TABLE "CoinTransfer" (
    "id" SERIAL NOT NULL,
    "userID" BIGINT NOT NULL,
    "guildID" BIGINT NOT NULL,
    "amount" BIGINT NOT NULL,
    "time" TIMESTAMP(3) NOT NULL,
    "detail" TEXT NOT NULL,

    CONSTRAINT "CoinTransfer_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Member" (
    "userID" BIGINT NOT NULL,
    "guildID" BIGINT NOT NULL,
    "experienceInGuild" BIGINT NOT NULL,
    "coinBalanceInGuild" BIGINT NOT NULL
);

-- CreateTable
CREATE TABLE "Guild" (
    "id" BIGINT NOT NULL,
    "announcementChannelID" BIGINT NOT NULL,
    "languageInGuild" TEXT NOT NULL,
    "notificationChannelID" BIGINT NOT NULL,
    "administratorRoleID" BIGINT NOT NULL,
    "timeZone" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "User_id_key" ON "User"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Member_userID_guildID_key" ON "Member"("userID", "guildID");

-- CreateIndex
CREATE UNIQUE INDEX "Guild_id_key" ON "Guild"("id");

-- AddForeignKey
ALTER TABLE "CoinTransfer" ADD CONSTRAINT "CoinTransfer_userID_guildID_fkey" FOREIGN KEY ("userID", "guildID") REFERENCES "Member"("userID", "guildID") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CoinTransfer" ADD CONSTRAINT "CoinTransfer_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Member" ADD CONSTRAINT "Member_userID_fkey" FOREIGN KEY ("userID") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Member" ADD CONSTRAINT "Member_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
