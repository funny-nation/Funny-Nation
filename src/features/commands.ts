import { ContextMenuCommandBuilder, SlashCommandBuilder } from '@discordjs/builders'
import getLanguage from '../language'
import { DBGuild } from '../models/DBGuild/DBGuild'
import commandSetup from '../utils/commandSetup'
import { ApplicationCommandType } from 'discord-api-types/v10'

async function setCommands (guild: DBGuild) {
  const language = getLanguage(guild.languageInGuild)
  // Put your commands right here in this list
  const commandsList = [
    new SlashCommandBuilder()
      .setName(language.commands.getMyProfile.name)
      .setDescription(language.commands.getMyProfile.desc),
    new ContextMenuCommandBuilder()
      .setName(language.mumble.mumble)
      .setType(ApplicationCommandType.User)
  ]
  await commandSetup(commandsList, guild)
}

export default setCommands
