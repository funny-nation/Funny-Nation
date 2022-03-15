import os
import time
import _thread
from threading import Thread

from loguru import logger
from discord import Client, Guild, VoiceChannel, VoiceState, Member
from pymysql import Connection
from typing import Dict, List

from src.model.makeDatabaseConnection import makeDatabaseConnection
from src.model.serverInfoManagement import addMinuteOnlineMinute
from src.model.userManagement import getUser, addNewUser, addMoneyToUser
from src.model.activityStatManagement import addActivityPointToUser, getActivityStatByUser, newActivityStatForUser
from src.utils.readConfig import getGeneralConfig, getCashFlowMsgConfig
from src.utils.runWhenBotStart.getMembersInVoiceStatesWhoAreActive import getMembersInVoiceStatesWhoAreActive
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
    activityPointPerMinuteInChannelInit: int = int(generalConfig['moneyEarning']['activityPointPerMinuteInChannelInit'])
    activityPointPerMinuteInChannelAddition: int = int(generalConfig['moneyEarning']['activityPointPerMinuteInChannelAddition'])
    maximumPeopleActivityPointPerMinuteInChannelAdd: int = int(generalConfig['moneyEarning']['maximumPeopleActivityPointPerMinuteInChannelAdd'])
    streamingAddition: int = int(generalConfig['moneyEarning']['streamingAddition'])
    while True:
        time.sleep(60)

        myGuild: Guild = self.guilds[0]
        voiceChannels: List[VoiceChannel] = myGuild.voice_channels
        db: Connection = makeDatabaseConnection()
        addMinuteOnlineMinute(db)
        logger.info("Scanning voice channels")
        for voiceChannel in voiceChannels:
            if myGuild.afk_channel is not None:
                if voiceChannel == myGuild.afk_channel:
                    continue
            voiceStates: Dict[int, VoiceState] = voiceChannel.voice_states

            membersInVoice, membersInStream = getMembersInVoiceStatesWhoAreActive(voiceStates, db)
            membersInVoice: List[Member]
            membersInStream: List[Member]

            totalNumberOfActiveMember = len(membersInVoice) + len(membersInStream)

            if totalNumberOfActiveMember == 0:
                continue

            if totalNumberOfActiveMember <= maximumPeopleActivityPointPerMinuteInChannelAdd:
                additionToUserInVoice = (totalNumberOfActiveMember - 1) * activityPointPerMinuteInChannelAddition
            else:
                additionToUserInVoice = (maximumPeopleActivityPointPerMinuteInChannelAdd - 1) * activityPointPerMinuteInChannelAddition



            activityPointEarnByMemberInVoice = activityPointPerMinuteInChannelInit + additionToUserInVoice

            for member in membersInVoice:
                if not addActivityPointToUser(db, member.id, activityPointEarnByMemberInVoice):
                    logger.error(f"Cannot add activity point for user {member}")

            for member in membersInStream:
                logger.debug(f"{member} earn {activityPointEarnByMemberInVoice + streamingAddition}")
                if not addActivityPointToUser(db, member.id, activityPointEarnByMemberInVoice + streamingAddition):
                    logger.error(f"Cannot add activity point for user {member}")
        db.close()
