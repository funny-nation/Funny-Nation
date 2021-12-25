from typing import List

from src.utils.poker.Card import Card


def sortCards(cards: List[Card]):
    for card in cards:
        if card.rank == 1:
            card.rank = 14

    for i in range(0, len(cards)):
        smallistCardPosition = i
        for j in range(i + 1, len(cards)):
            if cards[j].rank < cards[smallistCardPosition].rank:
                smallistCardPosition = j
        if i != smallistCardPosition:
            temp = cards[i]
            cards[i] = cards[smallistCardPosition]
            cards[smallistCardPosition] = temp

    for card in cards:
        if card.rank == 14:
            card.rank = 1


