import { client } from '../../../client'
import { GuildMember, Interaction, MessageEmbed } from 'discord.js'
import { RoleGroup } from './types/role-group'
import { newTabletop } from './storage'
import { getProcessControlActionRow } from './get-process-control-action-row'
import { DBGuild, getDbGuild } from '../../../models'
import { getLanguage } from '../../../language'
import { logger } from '../../../logger'
import { replyOnlyInteractorCanSee } from '../../../utils'

client.on('interactionCreate', async (interaction: Interaction) => {
  try {
    if (!interaction.isModalSubmit()) return

    if (interaction.customId !== 'roleAssignModalSubmission') return

    const rolesInput = interaction.fields.getTextInputValue('input')

    if (!rolesInput) return
    if (!interaction.member) return

    if (!interaction.channel) return
    if (!interaction.guild) return
    const dbGuild: DBGuild = await getDbGuild(interaction.guild.id)
    const language = getLanguage(dbGuild.languageInGuild)

    if (!(interaction.member instanceof GuildMember)) return

    const roles: string[] = rolesInput.split('\n')
    const roleGroups: RoleGroup[] = []
    let totalNumberOfPlayer = 0
    for (const role of roles) {
      if (role === '') continue
      const roleNameNumber = role.split(/[：:]/)
      if (roleNameNumber[0] === '') {
        replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.noRoleNameError)
        return
      }
      if (roleNameNumber.length !== 2) continue
      if (parseInt(roleNameNumber[1]) <= 0) continue
      const number = parseInt(roleNameNumber[1])
      if (isNaN(number)) {
        replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.noRoleNumberError)
        return
      }
      roleGroups.push({
        roleName: roleNameNumber[0],
        count: number
      })
      totalNumberOfPlayer += number
    }
    if (roleGroups.length < 2) {
      replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.oneTypeRoleError)
      // await interaction.reply(language.tabletopRoleAssign.oneTypeRoleError)
      return
    }

    const tabletop = newTabletop(interaction.channel, roleGroups, interaction.member, totalNumberOfPlayer, language)
    if (!tabletop) {
      replyOnlyInteractorCanSee(interaction, language.tabletopRoleAssign.channelUsed)
      // await interaction.reply(language.tabletopRoleAssign.channelUsed)
      return
    }

    const embedMsg = new MessageEmbed()
      .setTitle(`${language.tabletopRoleAssign.tabletopTitle} ${interaction.member.displayName}'s`)
      .setColor('#FF99CC')
      .setDescription(language.tabletopRoleAssign.tabletopDescription)

    for (const role of tabletop.roleGroups) {
      embedMsg.addField(role.roleName, `${role.count}`)
    }

    await interaction.reply({
      embeds: [embedMsg],
      components: [getProcessControlActionRow(language)]
    })
  } catch (e) {
    console.log(e)
    logger.error('Error in response to user create game operation')
  }
})
