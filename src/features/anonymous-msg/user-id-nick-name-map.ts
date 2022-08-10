import { names, uniqueNamesGenerator } from 'unique-names-generator'

const userIdNickNameMap = new Map<string, string>()

const getNickNameByUserId = (userID: string): string => {
  if (!userIdNickNameMap.has(userID)) {
    const nickName = uniqueNamesGenerator({
      dictionaries: [names]
    })
    userIdNickNameMap.set(userID, nickName)
    return nickName
  }
  return userIdNickNameMap.get(userID) as string
}

export { getNickNameByUserId }
