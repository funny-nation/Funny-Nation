/*
  Warnings:

  - The `languageInGuild` column on the `Guild` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- CreateEnum
CREATE TYPE "LanguageEnum" AS ENUM ('ChineseSimple', 'English');

-- AlterTable
ALTER TABLE "Guild" DROP COLUMN "languageInGuild",
ADD COLUMN     "languageInGuild" "LanguageEnum" NOT NULL DEFAULT 'English';
