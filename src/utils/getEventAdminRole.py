from discord import Guild, Role
from src.utils.readConfig import getEventAdminListConfig
from typing import List
from loguru import logger

async def getEventAdminRole(myGuild: Guild):
    eventConfig = getEventAdminListConfig()
    admainType = eventConfig.sections()
    admainEvent = []
    admainRoles = {}

    for admainType in admainType:
        admainEvent.append(int(admainType))
    roles: List[Role] = await myGuild.fetch_roles()
    for role in roles:
        for i in admainType:
            if eventConfig[i]['id'] == str(role.id):
                admainRoles[int(i)] = role

    return admainRoles

