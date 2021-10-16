import sys
import os
from io import BytesIO
from PIL import Image
from typing import List
from discord import File

from src.data.poker.Card import Card

pokerImages = []


def getPokerImagePath(rank: int, suit: int) -> str:
    return f"img{os.path.sep}cards{os.path.sep}{rank}_{suit}.png"


def initPokerImage():
    jokerImage = [Image.open(getPokerImagePath(0, 0)), Image.open(getPokerImagePath(0, 1))]
    pokerImages.append(jokerImage)
    for rank in range(1, 14):
        imagesForRank = []
        for suit in range(0, 4):
            imagesForRank.append(Image.open(getPokerImagePath(rank, suit)))
        pokerImages.append(imagesForRank)


initPokerImage()


def convertPilImageToDiscordFile(pilImage: Image) -> File:
    imageBin: BytesIO = BytesIO()
    pilImage.save(imageBin, format='PNG')
    imageBin.seek(0)
    dcFile: File = File(fp=imageBin, filename='card.png')
    imageBin.close()
    return dcFile


def getPokerImage(cards: List[Card]):
    if len(cards) == 1:
        imageReturn: Image = pokerImages[cards[0].rank][cards[0].suit]
        return convertPilImageToDiscordFile(imageReturn)

    imagesReturn = []
    for card in cards:
        imagesReturn.append(pokerImages[card.rank][card.suit])

    widths, heights = zip(*(i.size for i in imagesReturn))
    totalWith: int = sum(widths)
    height: int = max(heights)

    combinedCardImg = Image.new('RGB', (totalWith, height))

    offset = 0
    for img in imagesReturn:
        combinedCardImg.paste(img, (offset, 0))
        offset += img.size[0]

    return convertPilImageToDiscordFile(combinedCardImg)
