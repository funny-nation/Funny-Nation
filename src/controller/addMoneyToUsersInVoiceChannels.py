import sys
import os
import time
import _thread
from loguru import logger
sys.path.append(os.path.dirname(__file__) + '/../model')
import makeDatabaseConnection
import userManagement
import configparser

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')


def addMoneyToUserInVoiceChannels(self):
    _thread.start_new_thread(helperThreat, (self, ))


def helperThreat(self):
    while True:
        myGuild = self.guilds[0]
        voiceChannels = myGuild.voice_channels
        db = makeDatabaseConnection.makeDatabaseConnection()
        for voiceChannel in voiceChannels:
            if myGuild.afk_channel is not None:
                if voiceChannel == myGuild.afk_channel:
                    continue
            voiceStates = voiceChannel.voice_states
            for userID in voiceStates:

                # get user information
                userInfo = userManagement.getUser(db, userID)
                # Check if user existed
                if userInfo is None:
                    # not existed? create a new account
                    if not userManagement.addNewUser(db, userID):
                        logger.error(f"Cannot create new account to {userID} when sending message. ")
                    else:
                        logger.info(f"New account created for user {userID}")
                if voiceStates[userID].self_mute:
                    continue
                if voiceStates[userID].self_stream:
                    userManagement.addMoneyToUser(db, userID, config['moneyEarning']['perMinuteInVoiceWithStream'])
                    logger.info(f"Added {config['moneyEarning']['perMinuteInVoiceWithStream']} to {userID}")
                else:
                    userManagement.addMoneyToUser(db, userID, config['moneyEarning']['perMinuteInVoice'])
                    logger.info(f"Added {config['moneyEarning']['perMinuteInVoice']} to {userID}")
        db.close()
        time.sleep(60)
