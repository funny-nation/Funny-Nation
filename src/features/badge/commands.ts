import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { DBBadge } from '../../models/db-badge'

newCommand(async (language, guildID) => {
  const dbBadges: DBBadge[] = await DBBadge.fetchManyByGuild(guildID)
  const commandLang = language.badge.commands
  const comm = new SlashCommandBuilder()
    .setName(commandLang.name)
    .setDescription(commandLang.name)
    .addSubcommand( // Create
      subcommandGroup => subcommandGroup
        .setName(commandLang.create.name)
        .setDescription(commandLang.create.desc)
        .addStringOption(
          option => option
            .setName(commandLang.create.badgeNameOption)
            .setDescription(commandLang.create.badgeNameOption)
            .setMaxLength(20)
            .setRequired(true)
        )
        .addStringOption(
          option => option
            .setName(commandLang.create.emojiOption)
            .setDescription(commandLang.create.emojiOption)
            .setRequired(true)
        )
        .addStringOption(
          option => option
            .setName(commandLang.create.descOption)
            .setDescription(commandLang.create.descOption)
            .setMaxLength(1024)
            .setRequired(true)
        )
        .addIntegerOption(
          option => option
            .setName(commandLang.create.priceOption)
            .setDescription(commandLang.create.priceOption)
            .setRequired(true)
        )
        .addRoleOption(
          option => option
            .setName(commandLang.create.tagOption)
            .setDescription(commandLang.create.tagOption)
            .setRequired(true)
        )
    )
    .addSubcommand(
      subcommandGroup => subcommandGroup
        .setName(commandLang.list.name)
        .setDescription(commandLang.list.desc)
    )
    .addSubcommand(
      subcommandGroup => subcommandGroup
        .setName(commandLang.manageMyBadge.name)
        .setDescription(commandLang.manageMyBadge.desc)
    )
  comm.addSubcommand( // Remove
    subcommandGroup => subcommandGroup
      .setName(commandLang.remove.name)
      .setDescription(commandLang.remove.desc)
      .addStringOption(
        option => {
          const op = option
            .setName(commandLang.badge)
            .setDescription(commandLang.badge)
            .setRequired(true)
          if (dbBadges.length === 0) {
            op.addChoices({
              name: commandLang.remove.noBadgeYet,
              value: '0'
            })
          }
          for (const dbBadge of dbBadges) {
            op.addChoices({
              name: dbBadge.badgeData.name,
              value: String(dbBadge.badgeData.id)
            })
          }
          return op
        }
      )
  )
  comm.addSubcommand( // Buy
    subcommandGroup => subcommandGroup
      .setName(commandLang.buy.name)
      .setDescription(commandLang.buy.desc)
      .addStringOption(
        option => {
          const op = option
            .setName(commandLang.badge)
            .setDescription(commandLang.badge)
            .setRequired(true)
          if (dbBadges.length === 0) {
            op.addChoices({
              name: commandLang.remove.noBadgeYet,
              value: '0'
            })
          }
          for (const dbBadge of dbBadges) {
            op.addChoices({
              name: dbBadge.badgeData.name,
              value: String(dbBadge.badgeData.id)
            })
          }
          return op
        }
      )
      .addBooleanOption(
        option => option
          .setName(commandLang.buy.autoRenew)
          .setDescription(commandLang.buy.autoRenew)
          .setRequired(true)
      )
  )
  return comm
})
