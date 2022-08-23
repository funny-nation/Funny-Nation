const wait = (seconds: number): Promise<void> => new Promise((resolve) => {
  setTimeout(() => {
    resolve()
  }, seconds)
})

export { wait }
