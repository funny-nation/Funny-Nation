import { calculateLevelByExp } from '../calculate-level-by-exp'

test('Calculate level by exp', () => {
  expect(calculateLevelByExp(0)).toEqual(0)
  expect(calculateLevelByExp(9)).toEqual(1)
  expect(Number(calculateLevelByExp(-15.19).toFixed(1))).toEqual(-3.1)
})
