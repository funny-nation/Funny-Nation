import { getExpressApp } from '../express'

const app = getExpressApp()
app.get('/', (req, res) => {
  res.send('Hello World')
})
