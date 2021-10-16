class Table:
    def __init__(self, game: str):
        self.players = {}
        self.game = game

    def addPlayer(self, playerID: int):
        self.players[playerID] = {}

    def hasPlayer(self, playerID: int) -> bool:
        return playerID in self.players

    def dropPlayer(self, playerID: int):
        del self.players[playerID]
