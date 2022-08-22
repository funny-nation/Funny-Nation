const emojiRegEx = /^<.?:.*?:([0-9]+)>$/

const getEmojiIDFromStr = (str: string): string | null => {
  const regexResult = emojiRegEx.exec(str)
  if (regexResult) {
    return regexResult[1]
  }
  return null
}

export { getEmojiIDFromStr }
