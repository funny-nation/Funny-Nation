All the database models here

All models must follow the schema in ```/prisma/schema.prisma```

After you change the ```/prisma/schema.prisma```, make sure you run the migration. 

```shell
prisma migrate dev --name your_migration_name 
```

After you run the migration, you could import the data type from ```@prisma/client```. 

For example: 

```typescript
import { Guild } from '@prisma/client'
// Guild is the type of Guild defined in schema.prisma
```

Remember, you can only import the data type after you run the migration. 

If you don't know that is database migration, you need to read this [tutorial](https://www.prisma.io/docs/concepts/components/prisma-migrate), or ask me. 
