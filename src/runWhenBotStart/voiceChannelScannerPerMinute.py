import os
import time
import _thread
from threading import Thread

from loguru import logger
from discord import Client, Guild, VoiceChannel, VoiceState
from pymysql import Connection
from typing import Dict, List

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.model.userManagement import getUser, addNewUser, addMoneyToUser
from src.model.activityStatManagement import addActivityPointToUser, getActivityStatByUser, newActivityStatForUser
from src.utils.readConfig import getGeneralConfig, getCashFlowMsgConfig
generalConfig = getGeneralConfig()
cashFlowMsgConfig = getCashFlowMsgConfig()

def voiceChannelScannerPerMinute(self: Client):
    """
    Called when bot start
    This function would scan voice channel once per second, and add activity point to whom in voice channel.
    :param self:
    :return:
    """
    _thread.start_new_thread(__helperThreat, (self, ))


def __helperThreat(self: Client):
    """
    Thread helper function for addActivityPointWhenUserOnVoiceChannelPerMinute
    :param self:
    :return:
    """
    while True:
        time.sleep(60)
        myGuild: Guild = self.guilds[0]
        voiceChannels: List[VoiceChannel] = myGuild.voice_channels
        db: Connection = makeDatabaseConnection()
        logger.info("Finding who is in voice channel")
        for voiceChannel in voiceChannels:
            if myGuild.afk_channel is not None:
                if voiceChannel == myGuild.afk_channel:
                    continue
            voiceStates: Dict[int, VoiceState] = voiceChannel.voice_states
            for userID in voiceStates:

                # get user information
                userInfo: tuple = getUser(db, userID)
                # Check if user existed
                if userInfo is None:
                    if not addNewUser(db, userID):
                        logger.error(f"Cannot create new account to {userID} when sending message. ")
                    else:
                        logger.info(f"New account created for user {userID}")

                if not getActivityStatByUser(db, userID):
                    if not newActivityStatForUser(db, userID):
                        logger.error(f"Cannot create new activity stat for user {userID}")
                        continue

                # Check if user mute
                if voiceStates[userID].self_mute:
                    continue

                if voiceStates[userID].self_stream:
                    if not addActivityPointToUser(db, userID, generalConfig['moneyEarning']['activityPointPerMinuteInStream']):
                        logger.error(f"Cannot add activity point for user {userID}")
                    continue

                else:
                    if not addActivityPointToUser(db, userID, generalConfig['moneyEarning']['activityPointPerMinuteInChannel']):
                        logger.error(f"Cannot add activity point for user {userID}")
                    continue
        db.close()
