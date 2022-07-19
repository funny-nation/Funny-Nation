const isTest = () => {
  return process.env.ISTEST !== undefined
}
export default isTest
