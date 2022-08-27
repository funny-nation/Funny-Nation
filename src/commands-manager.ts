import { ContextMenuCommandBuilder, SlashCommandBuilder, SlashCommandSubcommandsOnlyBuilder } from '@discordjs/builders'
import { getLanguage, Language } from './language'
import { Guild } from 'discord.js'
import { logger } from './logger'
import { getDbGuild, LanguageEnum } from './models'

type CommandType = (SlashCommandBuilder | ContextMenuCommandBuilder | SlashCommandSubcommandsOnlyBuilder)

type CommandCreator = (language: Language, guildID: string) => CommandType | Promise<CommandType>

const commandsCreatorList: (CommandCreator)[] = []

const commandNamesSet = new Set<string>()

let refreshCommand = true
if (process.env.REFRESHCOMMAND) {
  if (process.env.REFRESHCOMMAND === 'false') {
    refreshCommand = false
  }
}

const newCommand = async (commandCreator: CommandCreator) => {
  const command: CommandType = await commandCreator(getLanguage(), '')
  if (command.name in commandNamesSet) {
    throw new Error(`Duplicated command name "${command.name}"`)
  }
  commandNamesSet.add(command.name)
  commandsCreatorList.push(commandCreator)
}

const setUpCommandsForGuild = async (languageEnum: LanguageEnum, discordGuild: Guild) => {
  const language = getLanguage(languageEnum)
  const dbGuild = await getDbGuild(discordGuild.id)
  const commandsData = []
  for (const commandCreator of commandsCreatorList) {
    const command: CommandType = await commandCreator(language, discordGuild.id)
    commandsData.push(command.toJSON())
  }
  if (refreshCommand) {
    await discordGuild.commands.set([])
    await discordGuild.commands.set(commandsData)
    await dbGuild.resetCommandsUpdatedAt()
    logger.info(`Commands for guild "${discordGuild.name}" updated`)
  } else {
    logger.info('Command refresh has been disabled')
  }
}

export { setUpCommandsForGuild, newCommand }
