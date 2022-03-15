# Funny Nation 开发指南

## 关于项目

本项目是一个Discord机器人项目，用于创造一个在Discord server中的元宇宙。

目前项目主要使用Python，基于Discord.py框架开发，以下是框架文档。

* [Discord.py API](https://discordpy.readthedocs.io/en/stable/api.html)
* [Discord.py Github Repo](https://github.com/Rapptz/discord.py)

在开发前，一定好好看看官方的例子以及文档。


## 开发规范

### 一些简单的

* 在开始前，你需要将这个库Fork一份到你的仓库中，然后你在你的仓库进行操作。

* 不要直接对main分支进行操作，写代码前请创建一个新的分支。

* 开发完成之后，并且测试后，请提交pull request，我会对代码进行审核。

* 请使用Pycharm的IDE开发，并且遵守Pycharm默认的Code style，不要把代码写的乱七八糟的。

* 一定要确保自己的代码有可读性，对于函数和变量要好好命名。


### 具体一点的

* 所有配置文件的读取都在```/src/utils/readConfig.py```中，需要获得哪个配置文件，只需要调用里面的函数即可。
* 如果可以单元测试的话，请在当前目录下创建一个```xxx_test.py```作为单元测试，然后在文件中定义一个test_()作为测试函数，具体请参考pytest文档。
* 所有机器人说的话（发给用户的消息），都写成模版放在Language.ini里面，然后在执行时调用配置文件，然后替换掉字符
  * 举个例子：
  ```
  await channel.send("转账成功，你收到了5元")  # 不要这样写
  
  # ---
  # 这样才对：
  
  msg = languageConfig['transfer']['transferSuccess'] \
      .replace("?@amount", f"{moneyTransfer / 100}")
  await channel.send(msg)
  ```
  * 并且记得，模版中的变量一定时以```?@xxx```来命名。


## 任务布置

我会在Issue里布置任务，并且会添加milestone，记得在due day之前提交我布置的任务。

发pull request的时候，记得勾选对应的milestone。

如果没有思绪的话，随时找我。


## 项目部署

### 方案1 - 手动部署

* 在```README.md```文件中，可以看到具体的部署过程

* 或者你可以在```.github/workflows/main.yml```来查看具体的部署过程

### 方案2 - Docker

* 本项目有Dockerfile来自动部署，需要把配置文件编辑好，然后就可以用Dockerfile创建镜像，具体也在```README.md```中。


## CI/CD

本项目包含持续集成，只针对main的分支中，使用的是Github Workflow。

具体文件在```.github/workflows/main.yml```


## 架构

这里的东西需要结合一下下面的`概念`部分来一起理解。

这个的整体结构类似于HTTP后端处理的路由结构，用户所发送的消息会被正则表达式匹配解析。如果这个消息是一条命令，那么它会被根据路由，传到特定的地方来进行解析并且处理。

在Bot启动时，会初始化

用户在公共频道发送任意消息之后，会调用pre-route中的函数```/src/controller/preRoute```，类似于给用户以每条消息1元加钱就是在这里实现的。

之后，会调用到router，位于```/src/controller/```下的四个router，分别处理四种不同的消息。如果router解析出该消息是一条指令，那么会调用```src/controller/routes```底下的函数。

所有系统的长驻内存信息都储存在Storage```/src/Storage.py```中，类似于Redux，这里包含了所有的状态信息，例如所有游戏的当前状态casino，正在等待的游戏玩家gamePlayerWaiting，用于公告的Channel，等等，相比于存入数据库，这里读取更快一些。

然后Storage本身是运行在```/src/Robot.py```中。

在```src/controller/routes```底下的函数，在被路由器调用后，一般要么去对Storage进行操作，要么对数据库进行操作。

系统在开始的时候，会启动一个子线程```/src/utils/addMoneyToUserInVoiceChannels.py```，用于监控语音频道中的玩家，然后每分钟会给语音频道里的玩家加钱。

同时，系统会每秒钟执行一次GamePlayerWaiting中的countdown()，用于为游戏玩家计时。


## 概念

**Model** - 对于数据库的操作，路径在```/src/model```。

* 当使用时，请

**Router** - 路由，类似于HTTP的路由，路由器位于```/src/controller/```下，总共四个路由器（公共消息路由，私聊消息路由，Reaction添加路由，Reaction删除路由），然后这四个路由器分别路由到```src/controller/routes```下面的模块中。

**pre-route** - 在执行Router之前所做的事情，例如为用户所发的每条消息加1块钱，位于```/src/controller/preRoute```下，在```/src/Robot.py```执行。

**Storage** - 位于```/src/Storage.py```，运行在```/src/Robot.py```，所有常驻内存数据都会常驻在此，储存这个Bot的状态信息，例如所有游戏的当前状态casino，正在等待的游戏玩家gamePlayerWaiting，用于公告的Channel，等等，相比于存入数据库，这里读取更快一些。

**Casino** - 包含所有关于游戏的类，位于```/src/utils/gamePlayerWaiting/GamePlayerWaiting.py```，运行在Storage里面，在Casino里面可以开若干个Table，然后Table内可以有Poker，一个Table代表一场游戏，会在routes下被调用。

**GamePlayerWaiting** - 位于```/src/utils/gamePlayerWaiting/GamePlayerWaiting.py```，用于给玩家计时的模块，系统每秒会执行countdown()一次，来实现计时功能。如果到时间了，会自动执行"超时"函数，同时会在剩下5秒时执行"warning"函数。


## 文件目录介绍

```/main.py```

* 运行的入口，在这里会调用```src/Robot.py```

```/src/Robot.py```

* 机器人所运行的类，定义了四种事件：收到公告频道消息，收到私聊消息，有人发了reaction，有人删除了reaction。
* 并且这运行了Storage。

```/src/Storage.py```

* Storage，在上面概念部分有介绍。

```/src/controller```

* 业务逻辑代码，包含了routers以及各种route，还有pre-route。

```/src/model```

* 对于数据库操作的代码。

```/src/utils```

* 各种杂七杂八的小工具以及一些helper functions。


## 最后

如果有些东西还是不明白的话，私聊我。

如果觉得这个文档写的不够好的话，你可以创建一个新的分支来修改本文档，然后发一个pull request给我。