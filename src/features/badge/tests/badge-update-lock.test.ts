import {badgeUpdateLock} from "../badge-update-lock";
import {wait} from "../../../utils/wait";

test('Test on badge update lock', async () => {
  badgeUpdateLock.lock('12345', 100)
  await wait(10)
  expect(badgeUpdateLock.isLock('12345')).toBeTruthy()
  await wait(200)
  expect(badgeUpdateLock.isLock('12345')).toBeFalsy()
})
