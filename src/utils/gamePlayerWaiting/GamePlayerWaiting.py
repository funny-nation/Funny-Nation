import threading
import configparser

from typing import Dict

config = configparser.ConfigParser()
config.read('config.ini')
secondWaitingPerPerson = int(config['gameWaitForPlayer']['secondWaitingPerPerson'])
secondOnWarning = int(config['gameWaitForPlayer']['secondOnWarning'])


class GamePlayerWaiting:

    def __init__(self):
        self.waiting: Dict[int, dict] = {}
        self.waitingLocker = threading.Lock()
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

    async def newWait(self, userID: int, timeoutFunction, warningFunction, timeOutSecond=secondWaitingPerPerson):
        """

        :param timeOutSecond:
        :param userID:
        :param timeoutFunction: async function
        :param warningFunction: async function
        :return:
        """
        self.waitingLocker.acquire()
        if userID in self.waiting:
            del self.waiting[userID]

        self.waiting[userID] = {
            'timeLeft': timeOutSecond,
            'timeoutFunction': timeoutFunction,
            'warningFunction': warningFunction
        }
        self.waitingLocker.release()

    async def removeWait(self, userID: int):
        print("remove wait")
        self.waitingLocker.acquire()
        print("aquired")
        if userID in self.waiting:
            del self.waiting[userID]
        self.waitingLocker.release()
        print("removed")

    async def countDown(self):
        self.waitingLocker.acquire()
        for userID in list(self.waiting):
            if self.waiting[userID]['timeLeft'] == 0:
                await self.waiting[userID]['timeoutFunction']()
                del self.waiting[userID]
                continue
            if self.waiting[userID]['timeLeft'] == secondOnWarning:
                await self.waiting[userID]['warningFunction']()

            self.waiting[userID]['timeLeft'] -= 1
        self.waitingLocker.release()
