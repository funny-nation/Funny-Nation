import { newCommand } from '../../commands-manager'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand(
  () => new SlashCommandBuilder()
    .setName('anonymous')
    .setDescription('Send anonymous message to this channel')
)
