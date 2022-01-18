from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from discord import Client, Guild, Role
from src.utils.fetchChannel import fetchAnnouncementChannel
from src.utils.getVipRoles import getVipRoles
from src.utils.readAdminList import getAdmin
from src.utils.readEventAdminList import getEventAdmin
from loguru import logger


class Storage:

    def __init__(self):
        self.boostedRole = None
        self.announcementChannel = None
        self.vipRoles = {}
        self.casino: Casino = Casino()
        self.gamePlayerWaiting = GamePlayerWaiting()
        self.admins = []
        self.eventList = []


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
        self.admins = await getAdmin(client)
        if len(self.admins) != 0:
            logger.info("Fetched Administrators")
        self.eventList = await getEventAdmin(client)
        if len(self.eventList) != 0:
            logger.info("Fetched eventAdministrators")
