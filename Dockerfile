FROM node:16

WORKDIR /usr/src/app

COPY ./src ./src

COPY ./prisma ./prisma

COPY ./package.json ./package.json

COPY ./jest.config.js ./jest.config.js

COPY ./tsconfig.json ./tsconfig.json

RUN npm install --omit=dev

RUN npm run build

CMD npx prisma migrate deploy && npm start
