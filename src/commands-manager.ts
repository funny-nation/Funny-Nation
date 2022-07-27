import { ContextMenuCommandBuilder, SlashCommandBuilder, SlashCommandSubcommandsOnlyBuilder } from '@discordjs/builders'
import { getLanguage, Language } from './language'
import { Guild, OAuth2Guild } from 'discord.js'
import { logger } from './logger'
import { getDbGuild, LanguageEnum } from './models'

type CommandType = (SlashCommandBuilder | ContextMenuCommandBuilder | SlashCommandSubcommandsOnlyBuilder)

type CommandCreator = (language: Language) => CommandType

const commandsCreatorList: (CommandCreator)[] = []

const commandNamesSet = new Set<string>()

const newCommand = (commandCreator: CommandCreator) => {
  const command: CommandType = commandCreator(getLanguage())
  if (command.name in commandNamesSet) {
    throw new Error(`Someone has already used the command name "${command.name}"`)
  }
  commandNamesSet.add(command.name)
  commandsCreatorList.push(commandCreator)
}

const setUpCommandsForGuild = async (languageEnum: LanguageEnum, discordGuild: Guild) => {
  const language = getLanguage(languageEnum)
  const dbGuild = await getDbGuild(discordGuild.id)
  const commandsData = []
  for (const commandCreator of commandsCreatorList) {
    const command: CommandType = commandCreator(language)
    commandsData.push(command.toJSON())
  }
  await discordGuild.commands.set([])
  await discordGuild.commands.set(commandsData)
  await dbGuild.resetCommandsUpdatedAt()
  logger.info(`Commands for guild "${discordGuild.name}" updated`)
}

export { setUpCommandsForGuild, newCommand }
