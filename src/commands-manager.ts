import { ContextMenuCommandBuilder, SlashCommandBuilder, SlashCommandSubcommandsOnlyBuilder } from '@discordjs/builders'
import { getLanguage, Language } from './language'
import { ApplicationCommand, Collection, Guild } from 'discord.js'
import { logger } from './logger'
import { getDbGuild, LanguageEnum } from './models'
import {
  RESTPostAPIChatInputApplicationCommandsJSONBody,
  RESTPostAPIContextMenuApplicationCommandsJSONBody
} from 'discord-api-types/v10'

type CommandType = (SlashCommandBuilder | ContextMenuCommandBuilder | SlashCommandSubcommandsOnlyBuilder)

type CommandCreator = (language: Language, guildID: string) => CommandType | Promise<CommandType>

const commandsCreatorList: (CommandCreator)[] = []

const commandNamesSet = new Set<string>()

const newCommand = async (commandCreator: CommandCreator) => {
  const command: CommandType = await commandCreator(getLanguage(), '')
  if (command.name in commandNamesSet) {
    throw new Error(`Duplicated command name "${command.name}"`)
  }
  commandNamesSet.add(command.name)
  commandsCreatorList.push(commandCreator)
}

const setUpCommandsForGuild = async (languageEnum: LanguageEnum, discordGuild: Guild) => {
  const commandsInGuild = await discordGuild.commands.fetch()
  if (commandsInGuild.size === 0) {
    await resetAllCommandsForGuild(discordGuild)
    return
  }
  await editCommandsForGuild(discordGuild)
  logger.info(`Commands for "${discordGuild.name}" updated`)
}

const editCommandsForGuild = async (discordGuild: Guild) => {
  const commandsDataInDict = await getCommandsDataInDict(discordGuild)
  const commandsDataInList = await getCommandsDataInArr(discordGuild)
  const commandsInGuild = await discordGuild.commands.fetch()

  for (const [commandID, command] of commandsInGuild) {
    if (!(command.name in commandsDataInDict)) {
      await discordGuild.commands.delete(commandID)
    }
  }
  await discordGuild.commands.set(commandsDataInList)
}

const getCommandsDataInDict = async (discordGuild: Guild): Promise<Map<string, (RESTPostAPIChatInputApplicationCommandsJSONBody | RESTPostAPIContextMenuApplicationCommandsJSONBody)>> => {
  const dbGuild = await getDbGuild(discordGuild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  const commandsData = new Map()
  for (const commandCreator of commandsCreatorList) {
    const command: CommandType = await commandCreator(language, discordGuild.id)
    commandsData.set(command.name, command.toJSON())
  }
  return commandsData
}

const getCommandsDataInArr = async (discordGuild: Guild): Promise<(RESTPostAPIChatInputApplicationCommandsJSONBody | RESTPostAPIContextMenuApplicationCommandsJSONBody)[]> => {
  const dbGuild = await getDbGuild(discordGuild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  const commandsData = []
  for (const commandCreator of commandsCreatorList) {
    const command: CommandType = await commandCreator(language, discordGuild.id)
    commandsData.push(command.toJSON())
  }
  return commandsData
}

const resetAllCommandsForGuild = async (discordGuild: Guild) => {
  const commandsData = await getCommandsDataInArr(discordGuild)
  await discordGuild.commands.set([])
  await discordGuild.commands.set(commandsData)
  const dbGuild = await getDbGuild(discordGuild.id)
  await dbGuild.resetCommandsUpdatedAt()
  logger.info(`All commands for guild "${discordGuild.name}" have been reset`)
}

export { setUpCommandsForGuild, newCommand }
