class Table:
    def __init__(self, game):
        self.players = {}
        self.game = game

    def addPlayer(self, playerID):
        self.players[playerID] = {}

    def hasPlayer(self, playerID):
        return playerID in self.players

    def dropPlayer(self, playerID):
        del self.players[playerID]
