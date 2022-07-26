/*
  Warnings:

  - The values [ChineseSimple] on the enum `LanguageEnum` will be removed. If these variants are still used in the database, this will fail.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "LanguageEnum_new" AS ENUM ('ChineseSimplified', 'English');
ALTER TABLE "Guild" ALTER COLUMN "languageInGuild" DROP DEFAULT;
ALTER TABLE "Guild" ALTER COLUMN "languageInGuild" TYPE "LanguageEnum_new" USING ("languageInGuild"::text::"LanguageEnum_new");
ALTER TYPE "LanguageEnum" RENAME TO "LanguageEnum_old";
ALTER TYPE "LanguageEnum_new" RENAME TO "LanguageEnum";
DROP TYPE "LanguageEnum_old";
ALTER TABLE "Guild" ALTER COLUMN "languageInGuild" SET DEFAULT 'English';
COMMIT;
