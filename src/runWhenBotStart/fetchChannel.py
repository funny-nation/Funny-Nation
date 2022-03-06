from src.utils.readConfig import getGeneralConfig
from discord import Guild, TextChannel
from typing import List

generalConfig = getGeneralConfig()


def fetchAnnouncementChannel(guild: Guild) -> TextChannel or None:
    if 'channelID' not in generalConfig['announcement']:
        return None

    channel: TextChannel = guild.get_channel(int(generalConfig['announcement']['channelID']))
    return channel
