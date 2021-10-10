import sys
import os
import time
import _thread
from loguru import logger

sys.path.append(os.path.dirname(__file__) + '/../model')
import makeDatabaseConnection
import userManagement
import cashFlowManagement
import configparser

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../../config.ini')


# start thread
def addMoneyToUserInVoiceChannels(self):
    _thread.start_new_thread(helperThreat, (self,))


def helperThreat(self):
    while True:
        myGuild = self.guilds[0]
        voiceChannels = myGuild.voice_channels
        db = makeDatabaseConnection.makeDatabaseConnection()
        logger.info("Finding who is in voice channel")
        for voiceChannel in voiceChannels:
            # skip afk channel
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
                        logger.error(f"Cannot create new account to {str(userID)} when sending message. ")
                    else:
                        logger.info(f"New account created for user {str(userID)}")
                # ignore muted user
                if voiceStates[userID].self_mute:
                    continue
                # streaming users gain more
                if voiceStates[userID].self_stream:
                    if userManagement.addMoneyToUser(db, userID, config['moneyEarning']['perMinuteInVoiceWithStream']):
                        logger.info(f"Added {config['moneyEarning']['perMinuteInVoiceWithStream']} to {str(userID)}")
                        if not cashFlowManagement.addNewCashFlow(db, userID,
                                                                 config['moneyEarning']['perMinuteInVoiceWithStream'],
                                                                 config['cashFlowMessage']['earnFromStream']):
                            logger.error(f"Cannot add to cash flow for {userID}")
                    else:
                        logger.error(f"Cannot add money to user {userID} while streaming")
                else:
                    if userManagement.addMoneyToUser(db, userID, config['moneyEarning']['perMinuteInVoice']):
                        logger.info(f"Added {config['moneyEarning']['perMinuteInVoice']} to {str(userID)}")
                        if not cashFlowManagement.addNewCashFlow(db, userID, config['moneyEarning']['perMinuteInVoice'],
                                                                 config['cashFlowMessage']['earnFromVoice']):
                            logger.error(f"Cannot add to cash flow for {userID}")

        db.close()
        time.sleep(60)
