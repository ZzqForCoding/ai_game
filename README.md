# 编程对战平台介绍

[项目地址](https://github.com/ZzqForCoding/ai_game)


## 平台主要功能

此作品是基于Python开发语言使用Django后端框架与Vue3前端框架实现的一个Web网站平台，此平台主要是为了给具有编程能力的同学和算法竞赛选手提供的一个基于各种游戏的编程对战平台。用户在开始游戏前按照网站提供的代码编写说明写好针对特定游戏的代码，用户可以创建一局游戏，选择代码或者鼠标、键盘操作，然后用户点击开始匹配，平台会根据玩家的匹配分为该选手提供一个实力最接近的对手与之对战。匹配成功后，3s后进入游戏界面，若用户选择的是鼠标、键盘操作，则用户可根据游戏介绍中的操作方式控制该游戏的每局操作，若用户选择的是代码控制，则平台会为每名玩家提供一个对战代码评测器，平台会在每回合的操作时间内为用户计算一个该回合的最优操作。当一名用户有违法操作或游戏胜利，则游戏结束，给相应的玩家加减他们的匹配分。

## 平台辅助功能

为每名用户提供用户信息管理界面，代码管理界面，个人空间，聊天室，排行榜，用户数据分析。

1. 用户信息管理界面可让用户绑定手机号码，后续用户可使用该手机号码进行验证码登录，并提供修改头像操作
2. 代码管理界面可对当前用户的代码进行创建、修改、删除，并能针对代码进行调试操作，代码支持主流的三种语言，分别是C++、Java、Python3
3. 个人空间可提供给玩家交流的环境、增强平台活跃度
4. 聊天室可提供实时的消息对话功能
5. 排行榜课对用户进行匹配分数排行，增加平台竞技性
6.用户数据分析提供了网站数据及访问量图和用户语言熟练度图，能清晰地让用户了解到该平台的活跃度与个人代码熟练度

## 平台亮点功能：
• 匹配机制

• 对战代码评测器


• 使用代码控制游戏每回合的操作

• 可开放游戏接口，让用户具有为平台生产游戏的能力

## 平台目前支持游戏：

* 绕蛇
* 五子棋
* 黑白棋

<br>

## 游戏该如何操作？

* [网站介绍](https://aigame.zzqahm.top/intro/)

* [游戏介绍](https://aigame.zzqahm.top/game_intro/)

* [代码编写说明](https://aigame.zzqahm.top/codehelper/)

## 使用技术 

前端技术：`ES6`、`Canvas`、`Vue`、`Vue Router`、`Vuex`、`jQuery`、`Element Plus`、`Echarts`、`Vue3 Ace Editor`、`v-me-editor`；使用`SimpleUI`实现后台管理界面。

后端技术：`Python`、`Django`、`Django Channels`、`Django Rest FrameWork`、`Django_Rest_Framework_SimpleJwt`、`Thrift`等技术。

<br>

**提示**：本项目使用过java、Spring Boot、Spring Boot WebSocket、Spring Cloud、Spring Security、Mybatis Plus实现，项目地址：[kob](https://github.com/ZzqForCoding/king-of-bots)

## 设计思路

首先从前端页面来构思整个网站，分为网站介绍、游戏大厅、动态、排行榜、个人信息、我的空间、登录和注册等页面。


网站介绍：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;包括网站说明，游戏介绍，代码编写指南。普通用户只可浏览页面，管理员需要有额外的修改权限。三个页面内容使用MarkDown语法进行编写，使用到v-me-editor前端技术提供MarkDown编辑器功能。

<br>

游戏大厅：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;包括创建游戏，游戏回放列表，公共聊天室，网站流量图与用户语言熟练分析图。创建游戏与公共聊天室结合WebSocket技术进行实现(依据它的长连接特性)；游戏回放列表则访问后端提供的接口获取，并提供对战详情可查看对局回放；网站图表使用到了Apache Echarts技术进行实现，并访问后端接口画出图表。

<br>

动态：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;包括发布，删除，点赞，评论，转发，查看。六个功能都是通过Jquery局部更新技术实现动态的增删改查，并可通过用户头像跳转至用户空间。

<br>

排行榜：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;根据玩家分数对网站玩家进行分数排行，并提供 分页 与 跳转至我所在页数 功能，并可根据用户头像跳转至特定玩家空间。

<br>

个人信息：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;对玩家个人信息、头像、手机号等信息进行维护文本信息通过后端访问数据库进行保存；头像使用到阿里云oss对象存储并回调返回存储网址存储进数据库；手机号通过阿里云提供的短信服务实现，使用户能够绑定手机号，方便用户使用手机号作为账号或找回密码。

<br>

我的空间：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;包括对代码、游戏回放、个人动态的管理。代码包括创建、删除、修改、查看、调试等功能，并提供扩容，因为网站限制用户只能创建10个代码，用户可通过支付宝支付一定金额扩容至15个，使用到了支付宝沙箱技术，增删改查则是访问后端接口进行实现，调试功能是通过WebSocket、Thrift、Docket等技术实现；游戏回放与个人动态的管理则是查询个人玩家的回放与动态进行实现。

<br>

登录与注册：<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;提供qq第三方登录和手机验证码登录，并提供修改密码功能，此外防止机器人进行自动注册或登录，使用到了滑动验证的方式。


## 部署指南


### 环境说明：

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ubuntu 20.04

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Docker Engine

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Docker Compose

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;git


### 部署代码：

```
# 创建父级目录
mkdir ai_game && cd ai_game

# 拉取项目
git clone git@gitee.com:Dev_ZzQ/ai_game.git  

# 修改项目配置(nginx配置需要修改，redis配置可不修改)
cd conf

# 修改nginx配置文件与https所需要的证书(替换cert文件夹下)，务必修改为自己的域名与证书文件
vim nginx.conf

# 查看此文件夹是否存在docker-compose.yml文件
cd ../
ls

# 可查看docker-compose文件，修改ports端口，并一定要在云服务器中开放端口，修改volumes中的路径(zzq为我的用户名，因此要修改成你的用户名)
cat docker-compose.yml

# 部署项目
docker-compose up -d

# 查看容器
docker ps -a
```


**提示：** 此项目通过shell脚本实现了启动容器自启动项目，因此只要在上述命令查看到容器启动成功，则项目启动成功


### 常见问题

若redis写日志出现报错：`Redis:Failed opening .rdb for saving: Permission denied`，执行以下命令可解决

```bash
sudo chmod 777 /data
sudo chmod 777 /data/dump.rdb
•通过nginx.conf中配置的域名访问网站
```

### 查看容器内服务运行或日志

```
# 查看容器名或id
docker ps -a
# 可通过以下命令进入docker容器查看容器内项目的服务
docker exec -it 容器名或id /bin/bash
# 本容器内通过tmux管理多终端窗口，此命令用于进入tmux
tmux a
# 进入选择tmux页面，通过方向键上/下选择终端
ctrl + a + s
# 退出tmux终端
ctrl + a + d
# 退出容器容器
ctrl + p + q
```

