import time

from loguru import logger
import configparser
from datetime import datetime
import threading
from src.utils.casino.Casino import Casino
from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting
from src.utils.printMemoryStatus.printCasinoLog import printCasinoLog
from src.utils.printMemoryStatus.printGamePlayerWaiting import printGamePlayerWaiting
from src.utils.readConfig import getGeneralConfig
generalConfig = getGeneralConfig()
logPath = generalConfig['log']['path'] + generalConfig['log']['memoryLog']


class PrintMemoryLogThread(threading.Thread):
    def __init__(self, casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
        threading.Thread.__init__(self)
        self.casino = casino
        self.gamePlayerWaiting = gamePlayerWaiting

    def run(self) -> None:
        while True:
            printMemoryLog(self.casino, self.gamePlayerWaiting)
            time.sleep(60)


def printMemoryLog(casino: Casino, gamePlayerWaiting: GamePlayerWaiting):
    # now: datetime = datetime.utcnow()
    # currentTime: str = now.strftime("%Y-%m-%d")
    # logger.add(logPath + currentTime)
    printCasinoLog(casino, logger)
    printGamePlayerWaiting(gamePlayerWaiting, logger)


def test_printMemoryLog():
    casino = Casino()
    gamePlayerWaiting = GamePlayerWaiting()
    gamePlayerWaiting.waiting[123] = {}
    gamePlayerWaiting.waiting[456] = {}
    casino.tables[11111] = {}
    casino.tables[22222] = {}
    casino.onlinePlayer.append(123)
    casino.onlinePlayer.append(456)
    printMemoryLog(casino, gamePlayerWaiting)

