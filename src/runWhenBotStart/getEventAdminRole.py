from discord import Guild, Role
from src.utils.readConfig import getAdminListConfig
from typing import List
from loguru import logger

async def getEventAdminRole(myGuild: Guild):
    """

    :param myGuild:
    :return:
    dict{
        'roleName': role,
        'roleName': role
        }
    """
    eventConfig = getAdminListConfig()
    sections = eventConfig.sections()
    roles: List[Role] = await myGuild.fetch_roles()
    result = {}

    for section in sections:
        roleID = int(eventConfig[section]['id'])
        for role in roles:
            if roleID == role.id:
                result[section] = role
                break

    return result

