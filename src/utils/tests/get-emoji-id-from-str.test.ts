import {getEmojiIDFromStr} from "../get-emoji-id-from-str";


test('Get emoji ID from string', () => {
  expect(getEmojiIDFromStr('<:emoji_15:935949404072988773>')).toEqual('935949404072988773')
  expect(getEmojiIDFromStr('<a:bot_icon:1011092177620832416>')).toEqual('1011092177620832416')
  expect(getEmojiIDFromStr('<:emoji_1935949404072988773>')).toBeNull()
})
