-- CreateTable
CREATE TABLE "Badge" (
    "id" SERIAL NOT NULL,
    "emoji" TEXT NOT NULL,
    "desc" TEXT NOT NULL,
    "price" BIGINT NOT NULL,
    "roleIDRelated" TEXT NOT NULL,
    "guildID" TEXT NOT NULL,

    CONSTRAINT "Badge_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Badge" ADD CONSTRAINT "Badge_guildID_fkey" FOREIGN KEY ("guildID") REFERENCES "Guild"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
