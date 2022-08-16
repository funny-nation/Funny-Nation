import { client } from '../../client'
import { Interaction, MessageEmbed } from 'discord.js'
import { getDbGuild, getDbUser } from '../../models'
import { getLanguage } from '../../language'
import { names, uniqueNamesGenerator } from 'unique-names-generator'
import { logger } from '../../logger'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
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
    const embed = new MessageEmbed()
      .setDescription(`${dbUser.anonymousNickName}🫣:\n${anonymousMsg}`)
      .setColor('#FF99CC')
    if (mention) {
      await interaction.channel.send({
        content: mention.toString(),
        embeds: [embed]
      })
    } else {
      await interaction.channel.send({
        embeds: [embed]
      })
    }
  } catch (e) {
    console.log(e)
    logger.error('Error when sending anonymous message')
  }
})
