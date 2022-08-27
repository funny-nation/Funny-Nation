# Developer Guides Extension

There are some recommendation for building this bot. 

### Disable command reset

According to Discord official documentation, one Discord bot cannot create more than 200 commands per day. 

However, after each restart the application, all commands will be removed and recreate. 

That means, a Discord bot cannot be restarted more than 10 times per day. 

So, in your development, if you do not need to update your commands, please add an environment variable: 
```
REFRESHCOMMAND=false
```
This variable will disable the command update. 
