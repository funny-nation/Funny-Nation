import { ButtonInteraction } from 'discord.js'

const cleanTable = async (interaction: ButtonInteraction) => {
  await interaction.update({
    content: '^^',
    components: [],
    embeds: []
  })
}

export { cleanTable }
