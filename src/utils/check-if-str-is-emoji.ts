const emojiRegEx = /^<.?:.*?:[0-9]+>$/
export function checkIfStrIsEmoji (str: string) {
  return emojiRegEx.test(str)
}
