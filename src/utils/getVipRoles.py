from discord import Guild, Role
from src.readConfig import getVipTagsConfig
from typing import List
from loguru import logger

async def getVipRoles(myGuild: Guild):
    vipTagsConfig = getVipTagsConfig()
    vipLevelsFromConfig = vipTagsConfig.sections()
    vipLevels = []
    vipRoles = {}
    for vipLevelFromConfig in vipLevelsFromConfig:
        vipLevels.append(int(vipLevelFromConfig))
    if vipTagsConfig is None:
        return {}
    roles: List[Role] = await myGuild.fetch_roles()
    for role in roles:
        for i in vipLevelsFromConfig:
            if vipTagsConfig[i]['id'] == str(role.id):
                vipRoles[int(i)] = role
                logger.info(f"Fetched role of {vipTagsConfig[i]['name']}")

    return vipRoles