import { checkIfStrIsEmoji } from '..'

test('Check if string is emoji', () => {
  expect(checkIfStrIsEmoji('<:emoji_15:935949404072988773>')).toBeTruthy()
  expect(checkIfStrIsEmoji('<a:bot_icon:1011092177620832416>')).toBeTruthy()
  expect(checkIfStrIsEmoji('<123>')).toBeFalsy()
})
