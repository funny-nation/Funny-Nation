Put your new features here. 

### If you need to add a new feature, 
then create a new folder here, or put this feature in other's folder here. 

You need to describe your feature in README.md in the folder. 

### Rule of the folder
All feature folder must contain a ```README.md``` file and a ```index.ts```. ```README.md``` describe your features in plain text. ```index.ts``` file is the entry file of your code. 

Make sure that you edit ```/src/features/index.ts``` for importing your  ```index.ts``` file here. 

### If your feature needs commands set up, 

Create a file ```commands.ts``` under your feature folder, and import your ```commands.ts``` in your ```index.ts```
```typescript
// Your index.ts
import './commands'
```

Put your command builder in ```commands.ts``` like that:

```typescript
import { newCommand } from '../../commands-manager'
import { Language } from '../../language'
import { SlashCommandBuilder } from '@discordjs/builders'

newCommand((language: Language) => new SlashCommandBuilder()
  .setName(language.commands.getMyProfile.name)
  .setDescription(language.commands.getMyProfile.desc)
)
```


### Something more
If you need to set up your unit test, please create a new folder ```tests``` under your folder, then put your unit test file under the ```tests``` folder. Make sure your unit test name as ```xxx.test.ts```. Example: ```get-user-member-profile/tests/calculate-level-by-exp.test.ts```

If some part of your code is reusable (might be reused) in the future or in the other components, you could put that in ```/src/utils/``` folder. 


### If you still not sure how to code

I recommend you to read other's features before you create yours. 
