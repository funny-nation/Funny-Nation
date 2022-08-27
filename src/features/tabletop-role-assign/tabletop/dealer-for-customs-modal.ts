import { client } from '../../../client'
import { Interaction, MessageActionRow, Modal, ModalActionRowComponent, TextInputComponent } from 'discord.js'
import { TextInputStyles } from 'discord.js/typings/enums'
import { logger } from '../../../logger'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isCommand()) return

    if (interaction.commandName !== 'role-assign') return
    if (!interaction.guild) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)

    if (interaction.options.getSubcommand() !== language.tabletopRoleAssign.subcommandName) return

    const modal = new Modal()
      .setTitle('发牌器')
      .setCustomId('roleAssignModalSubmission')
      .addComponents(
        new MessageActionRow<ModalActionRowComponent>()
          .addComponents(
            new TextInputComponent()
              .setCustomId('input')
              .setLabel('Roles')
              .setRequired(true)
              .setStyle(TextInputStyles.PARAGRAPH)
              .setPlaceholder(language.tabletopRoleAssign.playIntroduction)
          )
      )
    await interaction.showModal(modal)
  } catch (e) {
    console.log(e)
    logger.error('Error when a user creating a role assign')
  }
})
