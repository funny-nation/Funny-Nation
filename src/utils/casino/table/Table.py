from discord import Message, Member
import uuid


class Table:
    def __init__(self, game: str, inviteMessage: Message, maxPlayer: int, owner: Member):
        self.players = {}
        self.game = game
        self.maxPlayer = maxPlayer
        self.gameStarted = False
        self.gameOver = False
        self.inviteMessage: Message = inviteMessage
        self.owner: Member = owner
        self.uuid = str(uuid.uuid1())

    def addPlayer(self, playerID: int) -> bool:
        if self.gameStarted:
            return False
        if self.getPlayerCount() >= self.maxPlayer:
            return False
        self.players[playerID] = {}
        return True

    def hasPlayer(self, playerID: int) -> bool:
        return playerID in self.players

    def dropPlayer(self, playerID: int):
        del self.players[playerID]

    def isInviteMessage(self, message: Message):
        return message == self.inviteMessage

    def getPlayerCount(self):
        return len(self.players)