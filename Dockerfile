FROM node:16

WORKDIR /usr/src/app

COPY ./src ./src

COPY ./prisma ./prisma

COPY ./package.json ./package.json

COPY ./jest.config.js ./jest.config.js

COPY ./tsconfig.json ./tsconfig.json

RUN npm install

RUN npm run build

CMD npx prisma migrate deploy

CMD npm start
