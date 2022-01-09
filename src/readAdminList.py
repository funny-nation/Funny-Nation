from discord import Client, Guild, Member, Permissions
from loguru import logger
from discord import Guild
import sys
from typing import List, Any
from src.readConfig import getAdminListConfig

async def getAdmin(self: Client) -> List[int]:
    adminConfig = getAdminListConfig()
    if adminConfig is None:
        return []
    admins = []
    for section in adminConfig.sections():
        admins.append(int(adminConfig[section]['id']))
    return admins