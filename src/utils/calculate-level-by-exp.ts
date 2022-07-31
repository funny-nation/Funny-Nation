const calculateLevelByExp = (exp: number): number => {
  return Math.sqrt(exp + 16) - 4
}

export { calculateLevelByExp }
