from discord import Message


class Table:
    def __init__(self, game: str, inviteMessage: Message):
        self.players = {}
        self.game = game
        self.inviteMessage: Message = inviteMessage

    def addPlayer(self, playerID: int):
        self.players[playerID] = {}

    def hasPlayer(self, playerID: int) -> bool:
        return playerID in self.players

    def dropPlayer(self, playerID: int):
        del self.players[playerID]

    def isInviteMessage(self, message: Message):
        return message == self.inviteMessage
