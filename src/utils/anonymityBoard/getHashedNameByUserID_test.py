from src.utils.anonymityBoard.getHashedNameByUserID import getHashedChineseNameByUserID

def test():
    result1 = getHashedChineseNameByUserID(218224168340399409)
    result2 = getHashedChineseNameByUserID(218224168340399409)
    assert result2 == result1

    result3 = getHashedChineseNameByUserID(21822416834039409)
    result4 = getHashedChineseNameByUserID(21822416834039409)

    assert result3 != result2
    assert result4 == result3