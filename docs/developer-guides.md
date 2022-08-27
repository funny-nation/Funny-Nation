# Developer Guides

Before reading this guide, you need to know:
* [How to create your own Discord bot and get a token](discord-bot-setup-tutorial/README.md)
* [Contributing Guidelines](../CONTRIBUTING.md)

### Every time when you start your coding
Make sure you: 
* Fetch the code from dev branch from this repository. 
* Pull the code from your GitHub.
* Do migration.

### Technical stack and tools

* [Typescript](https://www.typescriptlang.org/) - Programming Language
* [Nodejs](https://nodejs.org/en/) - Interpreter
* [Prisma](https://www.prisma.io/) - Database ORM Tool
* [Jest](https://jestjs.io/) - Testing Framework
* [DiscordJS](https://discord.js.org/#/) - Discord Bot Framework

### File Structure

```/src/``` - All the source code should be here. All modules here are running in singleton pattern and hold some data in memory. 

```/src/models/``` - Database model

```/src/utils/``` - Reusable components

```/src/language/``` - Language management

```/src/features/``` - Features, contains the business logics

```/prisma/``` - All prisma files including the prisma schema

```/docs/``` - Documentations

There are rules and instructions for each folder. You can find them in README.md under each folder. You need to read them. 
* [src/features](../src/features/README.md)
* [src/language](../src/language/README.md)
* [src/models](../src/models/README.md)

### Addition rules to style guideline

#### Naming

* All filenames must follow ```kebab-case``` (Lower case)
* In side the file, all codes must follow ```CamelCase```
* In prisma migration name, all words must follow ```snake_case``` (Lower case)

#### Export

* Do not use export default

```typescript
export default getLanguageSetting // ❌

export { getLanguageSetting } // ✅
```

* Export your modules in ```index.ts``` if needed

```typescript
// index.ts
export * from './file1'
export * from './file2'
```


### Client Listener

If you don't know what is client's listener, please read [DiscordJS Official Documentation](https://discord.js.org/#/).

When you add a new listener or develop on a listener, make sure you: 

* Add filters before the listener. 
  * if the event should not be handled by your component, make sure you just return and do nothing.

```typescript
// ✅
client.on('interactionCreate', async function (interaction: Interaction) {
  if (!interaction.isCommand()) return // Filter
  if (interaction.commandName !== 'your command') return // Filter
  // do something else
})
```

```typescript
// ❌
client.on('interactionCreate', async function (interaction: Interaction) {
  if (!interaction.isCommand()) {
    await interaction.reply('This is not a command')
    return
  }
  if (interaction.commandName !== 'your command') {
    await interaction.reply('This is not my command')
    return
  }
  // do something else
})
```


### Testing

Currently, DiscordJS does not provide any testing tool so that we cannot create test for this bot. We are working on it now. 

We only can test the bot manually. 

If you need to test your internal components, you can create your test file ```xxx.test.ts```, then execute ```npm test```. 

### Stage bot

Stage bot is the bot that is built by continuous deployment. When you successfully merge your code into ```dev``` branch, the stage bot will be rebuilt with the latest code. 

You could try and test the stage bot in [Funny Nation](https://discord.gg/uhAv4J4F7Z) Discord Server. 

The name of the stage bot is: ```Funny Nation Staging#4122```. You can invite this bot to any server; here is the [invite URL](https://discord.com/api/oauth2/authorize?client_id=925297057277820929&permissions=8&scope=bot%20applications.commands). 

### Database for development

I recommend you to run a postgres database in Docker. 

```shell
docker run -d \
	--name Postres \
	-e POSTGRES_USER=theUser \
	-e POSTGRES_PASSWORD=thePassword \
	-p 5432:5432 \
	postgres
```

After that, you can use this database with URL: 

```
postgresql://theUser:thePassword@localhost:5432/theUser
```

Remember to perform a migration before you start the Bot. 

### Create your first feature

Before you start coding, I recommend you to look at other features we built. 

1. Create a folder under the ```/src/features/```. 
2. Create a ```README.md``` file for describing your new feature in English. 
3. Create your entry file ```getDbMember.ts``` under your folder, then add an ```import``` statement in file ```/src/features/get-db-member.ts``` to import your ```getDbMember.ts```. 
4. In your file, you can import the ```client```, and add any listener you want.

```typescript
import client from 'path-to-client'

client.on('something', async function () {
    // do something here
})
```

### Developer guides extension

Here is the [extension of developer guides](./developer-guides-ext.md). 

There are some suggestion for your development. 
