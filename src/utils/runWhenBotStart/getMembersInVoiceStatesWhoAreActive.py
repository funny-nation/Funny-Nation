from discord import VoiceState, Member, Guild
from typing import List, Dict
from pymysql import Connection
from src.Storage import Storage
from src.model.activityStatManagement import getActivityStatByUser, newActivityStatForUser
from src.model.userManagement import getUser, addNewUser
from loguru import logger


def getMembersInVoiceStatesWhoAreActive(voiceStates: Dict[int, VoiceState], db: Connection) -> (List[Member], List[Member]):
    """

    :param voiceStates:
    :param db:
    :return:
    a tuple (members who in voice but not steaming, members who streaming)
    """
    storage: Storage = Storage()
    myGuild: Guild = storage.myGuild
    membersInVoice: List[Member] = []
    membersInStreaming: List[Member] = []

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

        voiceState = voiceStates[userID]

        # Check if member is online
        thisMember: Member = myGuild.get_member(userID)
        if str(thisMember.desktop_status) != 'online':
            continue

        # Check if user mute
        if voiceState.self_mute:
            continue

        if voiceState.self_stream:
            membersInStreaming.append(thisMember)
        else:
            membersInVoice.append(thisMember)

    return membersInVoice, membersInStreaming