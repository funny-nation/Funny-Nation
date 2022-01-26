from discord import Guild, Role
from src.utils.readConfig import getAdminListConfig
from typing import List
from loguru import logger

async def getEventAdminRole(myGuild: Guild):
    eventConfig = getAdminListConfig()
    adminTypes = eventConfig.sections()
    adminEvent = []
    adminRoles = {}

    for adminType in adminTypes:
        adminEvent.append(adminType)
    roles: List[Role] = await myGuild.fetch_roles()
    for role in roles:
        for i in adminTypes:
            if eventConfig[i]['id'] == str(role.id):
                adminRoles[i] = role

    return adminRoles

