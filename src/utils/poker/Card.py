import os


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return (self.rank == other.rank) and (self.suit == other.suit)

    def getString(self) -> str:
        if self.suit == 0:
            return f"方片{self.convertRankToStr(self.rank)}"
        if self.suit == 1:
            return f"梅花{self.convertRankToStr(self.rank)}"
        if self.suit == 2:
            return f"红桃{self.convertRankToStr(self.rank)}"
        if self.suit == 3:
            return f"黑桃{self.convertRankToStr(self.rank)}"

    def getCardImgPath(self):
        return f"img{os.path.sep}cards{os.path.sep}{self.rank}_{self.suit}.png"


    @staticmethod
    def convertRankToStr(rank: int) -> str:
        if rank == 11:
            return 'J'
        if rank == 12:
            return 'Q'
        if rank == 13:
            return 'K'
        if rank == 1:
            return 'A'
        return str(rank)
