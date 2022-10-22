import express, { Express } from 'express'
import { logger } from './logger'

const app: Express = express()
let port: number = 8080
if (process.env.PORT_FOR_WEB !== undefined) {
  const portFromEnv = Number(process.env.PORT_FOR_WEB)
  if (Number.isInteger(portFromEnv)) {
    port = portFromEnv
  }
}

app.listen(port, () => {
  logger.info(`Web service has started at http://localhost:${port}`)
})

const getExpressApp = (): Express => {
  return app
}

export { getExpressApp }
