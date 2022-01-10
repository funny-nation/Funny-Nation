from discord import Client, Guild, Member, Permissions
from loguru import logger

async def checkPermissions(self: Client) -> bool:
    myGuild: Guild = self.guilds[0]
    selfMember: Member = await myGuild.fetch_member(self.user.id)
    selfPermission: Permissions = selfMember.guild_permissions
    if not selfPermission.manage_roles:
        logger.error("Lack of Permission on managing rules")
        return False

    return True