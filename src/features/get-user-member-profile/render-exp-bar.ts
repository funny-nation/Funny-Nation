import { calculateLevelByExp } from '../../utils/calculate-level-by-exp'

const renderExpBar = (exp: number) => {
  const level = calculateLevelByExp(exp)
  const percentageOfExpInCurrentLevel = level % 1
  const numberOfPlusSign = percentageOfExpInCurrentLevel * 20
  const numberOfDashSign = 20 - numberOfPlusSign
  let bar = '|'
  for (let i = 0; i < numberOfPlusSign; i += 1) {
    bar += '+'
  }
  for (let i = 0; i < numberOfDashSign; i += 1) {
    bar += '-'
  }
  bar += '|'
  return bar
}

export { renderExpBar }
