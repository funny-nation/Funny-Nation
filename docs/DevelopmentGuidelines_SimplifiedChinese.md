# Funny Nation 开发指南

## 关于项目

本项目是一个Discord机器人项目，用于创造一个在Discord server中的元宇宙。

目前项目主要使用Python，基于Discord.py框架开发，以下是框架文档。

* [Discord.py API](https://discordpy.readthedocs.io/en/stable/api.html)
* [Discord.py Github Repo](https://github.com/Rapptz/discord.py)

在开发前，一定好好看看官方的例子以及文档。

开发时，请遵守以下代码规范

* [Code style guideline - Simplified Chinese](docs/CodeStyleGuidelines_SimplifiedChinese.md)

推荐用pycharm开发，python版本最好是3.8。

## 开发流程

#### 开始前

* 你会被分配一个Issue，这个issue通常包含所有你需要的信息，包括做什么feature，如何实现，涉及到的数据库，涉及到的模块，开发完成之后所需要提交到的分支，以及最重要的：due date。
* 如果有任何不懂的东西，立马提问。

#### 开始开发

* 你需要将这个库Fork一份到你的仓库中，然后你在你的仓库进行后面的操作。
* 新建一个分支，以你想要的方式命名。
* 建立配置文件，建立embed模版库
  * 把配置文件（config/）和embed模版文件（embedLib）所有，每个文件复制一份到当前文件夹，去掉后面的.example。
  * 例子```cp configs/config.ini.example configs/config.ini```
  * 然后修改需要修改的配置文件
* 写代码，写自己的测试。
* 写完了之后，且测试完了之后，push到你的库，然后发pull request到你的issue提到的分支。

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

在Bot启动时，会初始化，其中包含对于```Storage```的初始化，启动各种定时事件。

用户在公共频道发送任意消息之后

1. 会调用pre-route中的函数```/src/controller/preRoute```，类似于给用户以每条消息1元加钱就是在这里实现的。

2. 之后，会调用到router，位于```/src/controller/```下的四个router: 。

3. 如果router解析出该消息是一条指令，那么会调用```src/controller/routes```底下的模块。

所有系统的长驻内存信息都储存在Storage```/src/Storage.py```中，类似于Redux，单例模式运行，这里包含了所有的状态信息，例如所有游戏的当前状态casino，正在等待的游戏玩家gamePlayerWaiting，用于公告的Channel，等等，相比于存入数据库，这里读取更快一些。

所有对于数据库的操作都存放在```/src/model```底下。

在```src/controller/routes```底下的函数，在被路由器调用后，一般要么去对Storage进行操作，要么对数据库进行操作。

系统在开始的时候，会启动一个子线程```/src/utils/addMoneyToUserInVoiceChannels.py```，用于监控语音频道中的玩家，然后每分钟会给语音频道里的玩家加钱。

同时，系统会每秒钟执行一次GamePlayerWaiting中的countdown()，用于为游戏玩家计时。


## 概念

**Model** - 对于数据库的操作，路径在```/src/model```。
* 开发时，请确保每一个对于数据库的操作都有一个单元测试

**Router** - 路由器，类似于HTTP的路由，路由器位于```/src/controller/```下，总共四个路由器，然后这四个路由器分别路由到```src/controller/routes```下面的模块中。
* ```publicMsgRouter```(处理用户发送的公告频道消息)
* ```privateMsgRouter```（处理用户私聊发送给Bot的消息）
* ```msgReactionRouter```（处理用户往消息添加的Reaction）
* ```msgReactionDeleteRouter```（处理用户删除的Reaction）
* 这四个路由器分别处理用户的四种事件

**pre-route** - 执行在消息达到Router之前所做的事情
* 例如为用户所发的每条消息加1块钱，位于```/src/controller/preRoute```下，在```/src/Robot.py```执行。

**Storage** - 位于```/src/Storage.py```，在```/src/Robot.py```初始化，单例模式，所有常驻内存数据都会常驻在此，储存这个Bot的状态信息。
* 例如所有游戏的当前状态casino，正在等待的游戏玩家gamePlayerWaiting，用于公告的Channel，等等，相比于存入数据库，这里读取更快一些。
* 使用时，这里有一个例子
```python
from src.Storage import Storage # 倒入
storageInstance = Storage() # 创建一个实例
```

**Casino** - 包含所有关于游戏的类，单例模式，位于```/src/utils/gamePlayerWaiting/GamePlayerWaiting.py```
* 在Casino里面可以开若干个Table，然后Table内可以有Poker，一个Table代表一场游戏，会在routes下被调用。
* 调用

**GamePlayerWaiting** - 位于```/src/utils/gamePlayerWaiting/GamePlayerWaiting.py```，用于给玩家计时的模块，系统每秒会执行countdown()一次，来实现计时功能。如果到时间了，会自动执行"超时"函数，同时会在剩下5秒时执行"warning"函数。
