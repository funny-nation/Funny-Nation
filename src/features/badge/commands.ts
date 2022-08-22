import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'
import { DBBadge } from '../../models/db-badge'

newCommand(async (language, guildID) => {
  const dbBadges: DBBadge[] = await DBBadge.fetchByGuild(guildID)
  const comm = new SlashCommandBuilder()
    .setName('badge')
    .setDescription('badge')
    .addSubcommand( // Create
      subcommandGroup => subcommandGroup
        .setName('create')
        .setDescription('Create a new badge')
        .addStringOption(
          option => option
            .setName('name')
            .setDescription('name')
            .setRequired(true)
        )
        .addStringOption(
          option => option
            .setName('emoji')
            .setDescription('emoji')
            .setRequired(true)
        )
        .addStringOption(
          option => option
            .setName('description')
            .setDescription('desc')
            .setRequired(true)
        )
        .addIntegerOption(
          option => option
            .setName('price')
            .setDescription('price')
            .setRequired(true)
        )
        .addRoleOption(
          option => option
            .setName('tag')
            .setDescription('tag')
            .setRequired(true)
        )
    )
    .addSubcommand(
      subcommandGroup => subcommandGroup
        .setName('list')
        .setDescription('List all badge')
    )
    .addSubcommand(
      subcommandGroup => subcommandGroup
        .setName('my-manage')
        .setDescription('Manage my badge')
    )
  if (dbBadges.length === 0) {
    return comm
  }
  comm.addSubcommand( // Remove
    subcommandGroup => subcommandGroup
      .setName('remove')
      .setDescription('Remove a badge')
      .addStringOption(
        option => {
          const op = option
            .setName('badge')
            .setDescription('badge')
            .setRequired(true)
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
      .setName('buy')
      .setDescription('Buy a badge')
      .addStringOption(
        option => {
          const op = option
            .setName('badge')
            .setDescription('badge')
            .setRequired(true)
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
          .setName('auto-renew')
          .setDescription('auto-renew')
          .setRequired(true)
      )
  )
  return comm
})
