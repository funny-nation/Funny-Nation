import sys
import threading
import time
import _thread
import asyncio
import os

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# secondWaitingPerPerson = int(config['gameWaitForPlayer']['secondWaitingPerPerson'])
# secondOnWarning = int(config['gameWaitForPlayer']['secondOnWarning'])
secondWaitingPerPerson = 5
secondOnWarning = 2
waiting = {}
waitingLocker = threading.Lock()
"""
waiting structure
{
    userID: int: {
        timeLeft: int, 
        timeoutFunction: function, 
        warningFunction: function
        
    }
}

"""


def newWait(userID: int, timeoutFunction, warningFunction):
    """

    :param userID:
    :param timeoutFunction: async function
    :param warningFunction: async function
    :return:
    """
    waitingLocker.acquire()
    if userID in waiting:
        del waiting[userID]

    def timeOutExe():
        asyncio.run(timeoutFunction())

    def warningExe():
        asyncio.run(warningFunction())

    waiting[userID] = {
        'timeLeft': secondWaitingPerPerson,
        'timeoutFunction': timeOutExe,
        'warningFunction': warningExe
    }
    waitingLocker.release()


class CountDownThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        while True:
            countDown()
            time.sleep(1)


def countDown():
    waitingLocker.acquire()
    for userID in list(waiting):
        if waiting[userID]['timeLeft'] == 0:
            _thread.start_new_thread(waiting[userID]['timeoutFunction'], ())
            del waiting[userID]
            continue
        if waiting[userID]['timeLeft'] == secondOnWarning:
            _thread.start_new_thread(waiting[userID]['warningFunction'], ())

        waiting[userID]['timeLeft'] -= 1
    waitingLocker.release()


def startPlayerWaitingThread():
    waitingThread = CountDownThread()
    waitingThread.start()


def test():
    startPlayerWaitingThread()

    async def callBack():
        print("Done")
        time.sleep(1)
        assert (12345678 in waiting) is False
        print("No error, please manually quit")

    async def warning():
        print("On warning")

    newWait(12345678, callBack, warning)
