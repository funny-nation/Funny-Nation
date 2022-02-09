from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from discord import Client, Guild, Role
from src.utils.fetchChannel import fetchAnnouncementChannel
from src.utils.getVipRoles import getVipRoles
from src.utils.getEventAdminRole import getEventAdminRole
from loguru import logger


class Storage:

    def __init__(self):
        self.boostedRole = None
        self.announcementChannel = None
        self.vipRoles = {}
        self.casino: Casino = Casino()
        self.gamePlayerWaiting = GamePlayerWaiting()
        self.adminRole = {}


    async def initialize(self, client: Client):
        myGuild: Guild = client.guilds[0]
        self.boostedRole: Role = myGuild.premium_subscriber_role
        if self.boostedRole is not None:
            logger.info("Fetched boosting role")
        self.announcementChannel = fetchAnnouncementChannel(myGuild)
        if self.announcementChannel is not None:
            logger.info("Fetched Announcement Channel")
        self.vipRoles = await getVipRoles(myGuild)
        if len(self.vipRoles) != 0:
            logger.info("Fetched VIP roles")
        self.adminRole = await getEventAdminRole(myGuild)
        logger.info(self.adminRole)
        if len(self.adminRole) != 0:
            logger.info("Fetched Administrators")
