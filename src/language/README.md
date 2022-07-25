Language library is here

How to use:

### If you need to get the language for a word:

```typescript
import getLanguage from "./get-language"
import {Language} from "./language"
import {DBGuild} from "./db-guild";

const languageEnum = guild.languageInGuild
const aWord = getLanguage(languageEnum).xx.inXXX
```

### If you need to set a new word, then

First, you need to change the structure of type in ```language.d.ts```; add anywhere you want. 

Then, you need to edit for each language files such as ```english-language.ts```. 

If you don't know the words in different languages, ask other team members. 

### If you need to add a new language, then

1. Open the file ```/prisma/schema.prisma```; you would find ```enum LanguageEnum```. Add the new name of your language there. 
2. Add a language file such as ```english-language.ts``` under the ```/src/language/``` folder. Make sure that you export the language in that file. 
3. Edit the file ```/src/language/get-db-member.ts```; add a switch statement for your language. 
