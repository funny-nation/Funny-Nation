import { client } from '../../client'
import { Interaction } from 'discord.js'
import { getDbGuild, getDbUser } from '../../models'
import { getLanguage } from '../../language'
import { names, uniqueNamesGenerator } from 'unique-names-generator'

client.on('interactionCreate', async (interaction: Interaction) => {
  if (!interaction.isCommand()) return
  if (!interaction.guild) return
  if (!interaction.user) return
  if (!interaction.channel) return

  if (interaction.commandName !== 'anonymous') return
  const dbGuild = await getDbGuild(interaction.guild.id)
  const language = getLanguage(dbGuild.languageInGuild)
  if (interaction.options.getSubcommand() !== language.anonymousMsg.commands.send.name) return
  const anonymousMsg = interaction.options.getString(language.anonymousMsg.commands.send.MsgOptionName)
  if (!anonymousMsg) return

  const dbUser = await getDbUser(interaction.user.id)
  if (!dbUser.anonymousNickName) {
    const newNickName = uniqueNamesGenerator({
      dictionaries: [names]
    })
    await dbUser.setAnonymousNickName(newNickName)
  }
  await interaction.deferReply({ ephemeral: true })
  await interaction.editReply('^ ^')
  const mention = interaction.options.getUser(language.anonymousMsg.commands.send.UserOptionName)
  const mentionMsg = mention ? '\n' + mention.toString() : ''
  await interaction.channel.send(`\`${dbUser.anonymousNickName}\`🫣:${mentionMsg}\n\`\`\`${anonymousMsg}\`\`\``)
})
