class Table:
    def __init__(self, game):
        self.players = {}
        self.game = game

    def addPlayer(self, playerID):
        self.players[playerID] = {}

    def dropPlayer(self, playerID):
        del self.players[playerID]
