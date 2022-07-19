import winston, { format } from 'winston'

const myFormat = format.printf((info) => {
  return `${info.timestamp} | ${info.level}: ${info.message}`
})

const logger = winston.createLogger({
  level: 'info',
  format: format.combine(
    winston.format.colorize({
      all: true
    }),
    format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    myFormat
  ),
  transports: []
})

switch (process.env.NODE_ENV) {
  case undefined:
    logger.add(new winston.transports.Console({ level: 'verbose' }))
    break
  case 'production':
    logger.add(new winston.transports.Console())
}

export default logger
