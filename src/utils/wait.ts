const wait = (millisecond: number): Promise<void> => new Promise((resolve) => {
  setTimeout(() => {
    resolve()
  }, millisecond)
})

export { wait }
