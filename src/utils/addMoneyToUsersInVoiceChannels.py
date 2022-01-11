import os
import time
import _thread

from loguru import logger
from discord import Client, Guild, VoiceChannel, VoiceState
from pymysql import Connection
from typing import Dict, List

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.model.userManagement import getUser, addNewUser, addMoneyToUser
from src.model.cashFlowManagement import addNewCashFlow
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def addMoneyToUserInVoiceChannels(self: Client):
    _thread.start_new_thread(helperThreat, (self, ))


def helperThreat(self: Client):
    while True:
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
                    # not existed? create a new account
                    if not addNewUser(db, userID):
                        logger.error(f"Cannot create new account to {userID} when sending message. ")
                    else:
                        logger.info(f"New account created for user {userID}")
                if voiceStates[userID].self_mute:
                    continue
                if voiceStates[userID].self_stream:
                    if addMoneyToUser(db, userID, int(config['moneyEarning']['perMinuteInVoiceWithStream'])):
                        logger.info(f"Added {config['moneyEarning']['perMinuteInVoiceWithStream']} to {userID}")
                        if not addNewCashFlow(db, userID, int(config['moneyEarning']['perMinuteInVoiceWithStream']), config['cashFlowMessage']['earnFromStream']):
                            logger.error(f"Cannot add to cash flow for {userID}")
                    else:
                        logger.error(f"Cannot add money to user {userID} while streaming")
                else:
                    if addMoneyToUser(db, userID, int(config['moneyEarning']['perMinuteInVoice'])):
                        logger.info(f"Added {config['moneyEarning']['perMinuteInVoice']} to {userID}")
                        if not addNewCashFlow(db, userID, int(config['moneyEarning']['perMinuteInVoice']), config['cashFlowMessage']['earnFromVoice']):
                            logger.error(f"Cannot add to cash flow for {userID}")
        db.close()
        time.sleep(60)
