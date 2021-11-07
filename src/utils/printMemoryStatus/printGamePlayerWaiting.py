from src.utils.gamePlayerWaiting.GamePlayerWaiting import GamePlayerWaiting


def printGamePlayerWaiting(gamePlayerWaiting: GamePlayerWaiting, log):
    msg = 'Players in wait: '
    for playerID in gamePlayerWaiting.waiting:
        msg += str(playerID) + " "

    log.info(msg)
