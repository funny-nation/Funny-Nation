let superUserID: string | null = null
if (process.env.SUPERUSERID) {
  superUserID = process.env.SUPERUSERID
}

export { superUserID }
