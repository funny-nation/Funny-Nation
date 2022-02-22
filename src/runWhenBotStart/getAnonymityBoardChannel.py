from src.utils.readConfig import getGeneralConfig
from discord import TextChannel, Client


def getAnonymityBoardChannel(client: Client) -> TextChannel or None:
    """
    Get anonymity board channel from configuration file
    :param client:
    :return: anonymity board channel
    """
    generalConfig = getGeneralConfig()
    anonymityBoardChannelID = int(generalConfig['anonymityBoard']['channelID'])
    channel: TextChannel = client.get_channel(anonymityBoardChannelID)
    return channel
