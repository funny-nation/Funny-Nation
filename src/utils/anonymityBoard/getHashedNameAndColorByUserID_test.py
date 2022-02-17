from src.utils.anonymityBoard.getHashedNameAndColorByUserID import getHashedChineseNameAndColorByUserID

def test():
    result1 = getHashedChineseNameAndColorByUserID(218224168340399409)
    result2 = getHashedChineseNameAndColorByUserID(218224168340399409)
    assert result2[0] == result1[0]
    assert result2[1] == result1[1]

    result3 = getHashedChineseNameAndColorByUserID(21822416834039409)
    result4 = getHashedChineseNameAndColorByUserID(21822416834039409)

    assert result3[0] != result2[0]
    assert result3[1] != result2[1]
    assert result4[0] == result3[0]
    assert result4[1] == result3[1]