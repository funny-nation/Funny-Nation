import threading
import time
import _thread
import asyncio

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
secondWaitingPerPerson = int(config['gameWaitForPlayer']['secondWaitingPerPerson'])
secondOnWarning = int(config['gameWaitForPlayer']['secondOnWarning'])
waiting = {

}
"""
waiting structure
{
    userID: int: {
        timeLeft: int, 
        timeoutFunction: function, 
        
    }
}

"""


def newWait(userID: int, timeoutFunction):
    waiting[userID] = {
        'timeLeft': secondWaitingPerPerson,
        'step': str,
        'timeoutFunction': timeoutFunction
    }


class CountDownThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        while True:
            countDown()
            time.sleep(1)


def countDown():
    for userID in waiting:
        if waiting[userID]['timeLeft'] == 0:
            _thread.start_new_thread(waiting[userID]['timeoutFunction'], ())
            del waiting[userID]
            continue

        waiting[userID]['timeLeft'] -= 1

