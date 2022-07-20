Language library is here

How to use:

### If you need to get the language for a word:

```typescript
import getLanguage from "./index"
import {Language} from "./Language"

const aWord = getLanguage('English').xx.inXXX
```

The language such as "English" are stored in database ```Guild``` model.

### If you need to set a new word, then

First, you need to change the structure of type in ```Language.d.ts```; add anywhere you want. 

Then, you need to edit for each language files such as ```english-language.ts```. 

If you don't know the words in different languages, ask other team members. 
