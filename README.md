# Funny Nations
<hr>

### About this
"Funny Nations" is a visual world that revolves around money within a Discord server. It is a Discord bot. There are games, activities, visual marriage, and real estate (channel) trade. 

Anyone inside the Discord server could earn money via playing games, participating in activities, sending messages, speaking in the voice channel, streaming, and using the money they earned to play games and buy real estate (channel).

If you could read Chinese, you could try this bot on this Discord server: 
https://discord.gg/CynuYmyMxD

Remember that you could only run that on one Discord server. This script does not support muti-server. 

### Get started
#### Environment
Require `python 3.8+` and `MySQL 8.0+`

Install dependency 
```
pip install -r requirements.txt
```

Create Configuration file
```
cp config.ini.example config.ini
```

Create migration configuration file
```
cp yoyo.ini.example yoyo.ini
```

Remember to edit the configuration files before use

Database migration
```
yoyo apply ./migrations
```

Start
```
python3.8 main.py
```
