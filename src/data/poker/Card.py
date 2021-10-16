class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def getString(self):
        if self.suit == 0:
            return f"方片{self.convertRankToStr(self.rank)}"
        if self.suit == 1:
            return f"梅花{self.convertRankToStr(self.rank)}"
        if self.suit == 2:
            return f"红桃{self.convertRankToStr(self.rank)}"
        if self.suit == 3:
            return f"黑桃{self.convertRankToStr(self.rank)}"

    def convertRankToStr(self, rank):
        if rank == 11:
            return 'J'
        if rank == 12:
            return 'Q'
        if rank == 13:
            return 'K'
        if rank == 1:
            return 'A'
        return str(rank)
