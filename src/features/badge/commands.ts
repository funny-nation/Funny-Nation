import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(() => {
  const comm = new SlashCommandBuilder()
    .setName('badge')
    .setDescription('badge')
    .addSubcommand( // Create
      subcommandGroup => subcommandGroup
        .setName('create')
        .setDescription('Create a new badge')
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
    .addSubcommand( // Remove
      subcommandGroup => subcommandGroup
        .setName('remove')
        .setDescription('Remove a badge')
        .addStringOption(
          option => option
            .setName('badge')
            .setDescription('badge')
            .setRequired(true)
        )
    )
    .addSubcommand( // Buy
      subcommandGroup => subcommandGroup
        .setName('buy')
        .setDescription('Buy a badge')
        .addStringOption(
          option => option
            .setName('badge')
            .setDescription('badge')
            .addChoices(
              {
                name: '<:emoji_11:935948891654877235>', value: '1'
              }
            )
            .setRequired(true)
        )
        .addBooleanOption(
          option => option
            .setName('auto-renew')
            .setDescription('auto-renew')
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
  return comm
})
