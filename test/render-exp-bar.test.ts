import renderExpBar from '../src/features/get-user-member-profile/render-exp-bar'

test('Render exp bar', () => {
  expect(renderExpBar(0)).toEqual('|--------------------|')
  expect(renderExpBar(9)).toEqual('|--------------------|')
  expect(renderExpBar(20)).toEqual('|--------------------|')

  expect(renderExpBar(40.25)).toEqual('|++++++++++----------|')
})
