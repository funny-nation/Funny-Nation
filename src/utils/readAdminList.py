from discord import Client
from typing import List
from src.utils.readConfig import getAdminListConfig

async def getAdmin(self: Client) -> List[int]:
    adminConfig = getAdminListConfig()
    if adminConfig is None:
        return []
    admins = []
    for section in adminConfig.sections():
        admins.append(int(adminConfig[section]['id']))
    return admins