import { client } from '../../client'
import { SlashCommandBuilder, SlashCommandStringOption } from '@discordjs/builders'
import { LanguageEnum } from '@prisma/client'
import { superUserID } from './super-user-id-from-env'
import { logger } from '../../logger'

client.on('ready', async () => {
  if (client.application === null) return
  if (!superUserID) {
    logger.info('No super user in this bot')
    return
  }
  logger.info(`${superUserID} is the super user in this bot`)

  const slashCommand = new SlashCommandBuilder()
    .setName('superuser')
    .setDescription('Super user command')

  slashCommand.addSubcommand(
    subcommand => subcommand
      .setName('demo-notification')
      .setDescription('Demo notification')
  )

  slashCommand.addSubcommand(
    subcommand => subcommand
      .setName('send-notification')
      .setDescription('Send notification to all guilds')
      .addStringOption(
        (option: SlashCommandStringOption) => {
          option.setName('language')
            .setDescription('Language you want to send notification for')
            .setRequired(true)
          for (const language in LanguageEnum) {
            option.addChoices({
              name: language, value: language
            })
          }
          return option
        }
      )
  )

  client.application.commands.set([
    slashCommand.toJSON()
  ])
})
