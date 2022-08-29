-- CreateTable
CREATE TABLE "MemberBadge" (
    "badgeID" INTEGER NOT NULL,
    "userID" TEXT NOT NULL,
    "guildID" TEXT NOT NULL,
    "expiredAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateIndex
CREATE UNIQUE INDEX "MemberBadge_badgeID_userID_guildID_key" ON "MemberBadge"("badgeID", "userID", "guildID");

-- AddForeignKey
ALTER TABLE "MemberBadge" ADD CONSTRAINT "MemberBadge_badgeID_fkey" FOREIGN KEY ("badgeID") REFERENCES "Badge"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "MemberBadge" ADD CONSTRAINT "MemberBadge_userID_guildID_fkey" FOREIGN KEY ("userID", "guildID") REFERENCES "Member"("userID", "guildID") ON DELETE RESTRICT ON UPDATE CASCADE;
