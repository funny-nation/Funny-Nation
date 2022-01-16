from discord import Client
from typing import List
from src.utils.readConfig import getEventAdminListConfig

async def getEventAdmin(self: Client) -> List[int]:
    adminConfig = getEventAdminListConfig()
    if adminConfig is None:
        return []
    eventAdmins = []
    for section in adminConfig.sections():
        eventAdmins.append(int(adminConfig[section]['id']))
    return eventAdmins