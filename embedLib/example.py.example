from discord import Embed


def getEmbed() -> Embed:
    embed = Embed()
    embed.title = "This is title"
    embed.description = "This supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```"
    embed.add_field(name="Name of the field", value="This is an inline field content", inline=True)
    embed.add_field(name="Name of the field", value="This is an another inline field content", inline=True)
    embed.add_field(name="Not inline field", value="This is not an inline field content", inline=False)
    embed.url = "https://google.com"
    embed.colour = 0xFF0000
    embed.set_author(name="Linbin Pang", url="https://google.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="This is the footer", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_image(url="https://www.teenet.me/wp-content/uploads/2022/01/funnyNation.png")

    return embed
