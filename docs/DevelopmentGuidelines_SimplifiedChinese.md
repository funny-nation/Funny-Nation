# Funny Nation 开发指南

## 关于项目

本项目是一个Discord机器人项目，用于创造一个在Discord server中的元宇宙。

目前项目主要使用Python，基于Discord.py框架开发，以下是框架文档。

* [Discord.py API](https://discordpy.readthedocs.io/en/stable/api.html)
* [Discord.py Github Repo](https://github.com/Rapptz/discord.py)

在开发前，一定好好看看官方的例子以及文档。

开发时，请遵守以下代码规范

* [Code style guideline - Simplified Chinese](docs/CodeStyleGuidelines_SimplifiedChinese.md)

这里有一个我开发红包功能的录像，如果需要的话可以参考

* [第一集](https://www.youtube.com/watch?v=zHTiDIoCNpk)
* [第二集](https://www.youtube.com/watch?v=idFxVovaue4)
* [第三集](https://www.youtube.com/watch?v=52na7WCnK5o)
* [第四集](https://www.youtube.com/watch?v=52na7WCnK5o)

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

