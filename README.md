# 编程对战平台

## 项目介绍

[docker hub](https://hub.docker.com/repository/docker/zzq10/ai_game/general)

此项目是基于五子棋、绕蛇、黑白棋进行游戏匹配，玩家可选择代码或键盘、鼠标进行操作，的一个编程对战平台，平台会执行用户所写代码，作为每回合的游戏操作，并因为玩家操作导致游戏地图不同，因此导致每回合输出不同，玩家需要编写一个通过地图与双方操作数据输入，输出一个最优决策。

<br>

本项目实现了匹配、游戏回放、联机对战、动态、Bot编写与调试、支付宝支付、上传头像和短信验证码等功能。包含前端技术：`es6`、`canvas`、`Vue`、`Vue Router`、`Vuex`、`Jquery`、`Element Plus`、`Echarts`、`Vue3 Ace Editor`、`v-me-editor`，后端技术包括`Python`、`Django`、`Django Channels`、`Django Rest FrameWork`、`Django_Rest_Framework_SimpleJwt`、`Thrift`等技术，并使用SimpleUI实现后台管理界面。

<br>

本项目使用过java、Spring Boot、Spring Boot WebSocket、Spring Cloud、Spring Security、Mybatis Plus实现，项目地址：[kob](https://git.acwing.com/study/project1/kob)

<br>

## 游戏该如何操作？

* [网站介绍](https://aigame.zzqahm.top/intro/)

* [游戏介绍](https://aigame.zzqahm.top/game_intro/)

* [代码编写说明](https://aigame.zzqahm.top/codehelper/)

<br>

## 游戏部署

**拉取项目至本地：**
```git
git clone git@git.acwing.com:ZzQ/aigameplatform.git
```
<br>

**通过dockerfile制作镜像、docker compose部署每个服务：**
```shell
cd docerk-compose.yml所在目录
docker-compose up -d
```

**注意：** `conf`文件夹下的nginx配置文件与redis配置文件有需要修改可以直接修改，nginx里配置了域名与https证书；容器可以通过`docker exec -it 容器名或id /bin/bash`命令进入容器，通过`tmux a`可查看正在运行服务

<br>

## 常见问题

若redis写日志出现报错：`Redis:Failed opening .rdb for saving: Permission denied`，执行以下命令可解决
```shell
sudo chmod 777 /data
sudo chmod 777 /data/dump.rdb
```
