import configparser
from discord import Guild, TextChannel
from typing import List

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def fetchGiftAnnouncementChannel(guild: Guild):
    if 'channel' not in config['gift']:
        return None

    allTextChannels: List[TextChannel] = guild.text_channels
    for channel in allTextChannels:
        if channel.name == config['gift']['channel']:
            return channel

    return None
