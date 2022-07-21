# Funny Nation

A money-centric "Meta-verse" Discord Bot

[![](https://github.com/funny-nation/Funny-Nation/actions/workflows/eslint.yml/badge.svg)](https://github.com/funny-nation/Funny-Nation/actions/workflows/eslint.yml)
[![](https://github.com/funny-nation/Funny-Nation/actions/workflows/test.yml/badge.svg)](https://github.com/funny-nation/Funny-Nation/actions/workflows/test.yml)
[![](https://github.com/funny-nation/Funny-Nation/actions/workflows/test-on-start.yml/badge.svg)](https://github.com/funny-nation/Funny-Nation/actions/workflows/test-on-start.yml)
[![](https://github.com/funny-nation/Funny-Nation/actions/workflows/to-docker-hub.yml/badge.svg)](https://github.com/funny-nation/Funny-Nation/actions/workflows/to-docker-hub.yml)
[![Our Discord](https://img.shields.io/badge/Chat-Discord-7289da)](https://discord.gg/uhAv4J4F7Z)

### About this Discord bot

Funny Nation is a Discord bot that makes Discord servers into a "metaverse." 

People could earn coins and experience points by the activity on Discord channels (either voice or text), and people could exchange coins for tradings. 

Also, people could play games via interaction with this bot to earn money (sometimes to lose money).

There are a lot of features and ideas that are still in development. Let me know if you have any cool ideas.

### Before Deploy your bot

You need to set up a Discord application and get a Discord bot token. If you don't know how to do that, please read the tutorial [at this link](docs/discord-bot-setup-tutorial/README.md). 


### Deploy with Docker

Requirements: 
* Docker
* A PostgresSQL database with URL - Example: ```postgresql://username:password@database.url:5432/databasename```
* A Discord Bot Token

#### From Docker hub

```shell
docker run --name funnynation \
 -e DATABASE_URL="postgresql://your-postgres-database-url" \
 -e DISCORD_TOKEN="your-discord-token" \
 -d plbin97/funny-nation
```

#### Or build your own Docker Image

```shell
docker build -t funnynation .
```

```shell
docker run --name funnynation \
 -e DATABASE_URL="postgresql://your-postgres-database-url" \
 -e DISCORD_TOKEN="your-discord-token" \
 -d funnynation
```

### Deploy with Nodejs

Requirements:
* An Node environment, ```16.x``` recommended
* A PostgresSQL database with URL - Example: ```postgresql://username:password@database.url:5432/databasename```
* A Discord Bot Token

#### Step1: Install dependency
```shell
npm install
```

#### Step2: Build
```shell
RUN npm run build
```

#### Step3: Database Migration

```shell
DATABASE_URL="postgresql://your-postgres-database-url" \
npx prisma migrate deploy
```

#### Step4: Run
```shell
DATABASE_URL="postgresql://your-postgres-database-url" \
DISCORD_TOKEN="your-discord-token" \
npm start
```

### Contact Us

If you have any questions, or you want to join our team. 

You can talk to us via this [Discord Server](https://discord.gg/uhAv4J4F7Z). 

### Contribution

If you want to contribute to this project, please make sure that you have read:
* [Contributing Guidelines](CONTRIBUTING.md)
* [Developer Guide](docs/developer-guides.md)
