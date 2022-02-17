import hashlib
from src.utils.readConfig import getMajorConfig
from src.Storage import Storage
from typing import List

headRange = {
	'start': 0xb0,
	'end': 0xd7
}

bodyRange = {
	'start': 0xa1,
	'end': 0xf0
}

headRangeInt = headRange['end'] - headRange['start']
bodyRangeInt = bodyRange['end'] - bodyRange['start']

def getHashedChineseNameAndColorByUserID(userID: int) -> List[str]:
	storage = Storage()
	hashedUserID: int = int(hashlib.sha256(str(userID).encode('utf-8')).hexdigest(), 16)
	hashedUserID += storage.randomPrivateShiftForAnonymityBoard
	hashedUserIDForHead: int = hashedUserID % 100 # get last two digits
	hashedUserIDForBody: int = hashedUserID % 10000 // 100 ## get from last four digit to last two digits

	hashedUserIDForColor: int = hashedUserID // 1000000
	hexedUserID = hex(hashedUserIDForColor)
	hexedColor = str(hexedUserID)[-6:]

	headShift: int = int(headRangeInt * (hashedUserIDForHead / 99))
	bodyShift: int = int(bodyRangeInt * (hashedUserIDForBody / 99))
	resultHead: int = headRange['start'] + headShift
	resultBody: int = bodyRange['start'] + bodyShift
	hashedChineseWord = bytes.fromhex(f'{resultHead:x}{resultBody:x}').decode('gb2312')
	return ['小' + hashedChineseWord, hexedColor]