from discord import Client, Guild, Member, Permissions
from loguru import logger
from discord import Guild
import sys
from typing import List, Any


async def getAdmin(self: Client) -> List[List[Any]]:
    admins = []
    with open("adminList.txt", "r") as fileA:
        for line in fileA:
            admins.append(list(line.strip("\n").split(".")))
    return admins