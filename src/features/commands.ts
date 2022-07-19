import { SlashCommandBuilder } from '@discordjs/builders'
import getLanguage from '../language'
import { DBGuild } from '../models/DBGuild/DBGuild'
import commandSetup from '../utils/commandSetup'

async function setCommands (guild: DBGuild) {
  const language = getLanguage(guild.languageInGuild)
  const commandsList = [
    new SlashCommandBuilder()
      .setName(language.commands.getMyProfile.name)
      .setDescription(language.commands.getMyProfile.desc)
  ]
  await commandSetup(commandsList, guild)
}

export default setCommands
