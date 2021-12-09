import os


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self._value: int = (rank << 2) + suit
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

    @property
    def rank(self) -> int:
        return self._value >> 2

    @property
    def suit(self) -> int:
        return self._value & 3

    def __lt__(self, other):
        return int(self) < int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __int__(self):
        return self._value

    def dto(self):
        return self.rank, self.suit