FROM node:16

WORKDIR /usr/src/app

COPY . ./

RUN npm install --omit=dev

RUN npm run build

CMD npx prisma migrate deploy && npm start
