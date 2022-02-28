from src.utils.readConfig import getGeneralConfig
from discord import Guild, TextChannel
from typing import List

generalConfig = getGeneralConfig()


def fetchAnnouncementChannel(guild: Guild):
    if 'channel' not in generalConfig['announcement']:
        return None

    allTextChannels: List[TextChannel] = guild.text_channels
    for channel in allTextChannels:
        if channel.name == generalConfig['announcement']['channel']:
            return channel

    return None
