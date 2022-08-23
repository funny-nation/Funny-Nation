import {
  ApplicationCommand,
  Guild,
  ApplicationCommandChoicesOption,
  ApplicationCommandOptionChoiceData
} from 'discord.js'

const locateCommand = (guild: Guild, commandName: string): ApplicationCommand | null => {
  const commandsCache = guild.commands.cache
  let targetCommand: ApplicationCommand | null = null
  for (const [, command] of commandsCache) {
    if (command.name === commandName) {
      targetCommand = command
      break
    }
  }
  return targetCommand
}

/**
 * Update choice for a subcommand of a guild.
 * The original choices would be removed, and replaced by choices in parameters.
 * @param guild
 * @param commandName
 * @param subCommandName
 * @param optionName
 * @param choices
 */
const updateCommandOptionChoicesForGuild = async (guild: Guild, commandName: string, subCommandName: string, optionName: string, choices: ApplicationCommandOptionChoiceData[]): Promise<boolean> => {
  const targetCommand = locateCommand(guild, commandName)
  if (!targetCommand) return false

  let subCommand = null

  for (const optionOfCommand of targetCommand.options) {
    if (optionOfCommand.name === subCommandName && optionOfCommand.type === 'SUB_COMMAND') {
      subCommand = optionOfCommand
      break
    }
  }
  if (!subCommand) return false
  if (!subCommand.options) return false

  let option = null

  for (const optionOfSubCommand of subCommand.options) {
    if (optionOfSubCommand.name === optionName) {
      option = optionOfSubCommand
      break
    }
  }
  if (!option) return false
  if (!Object.prototype.hasOwnProperty.call(option, 'choices')) return false
  option = option as ApplicationCommandChoicesOption
  option.choices = []
  for (const newChoice of choices) {
    option.choices.push(newChoice)
  }
  await guild.commands.edit(targetCommand.id, {
    options: targetCommand.options
  })
  return true
}

export { updateCommandOptionChoicesForGuild }
