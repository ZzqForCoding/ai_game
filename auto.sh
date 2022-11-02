#! /bin/bash
USER_PASSWORD=Zcbm980528
USERNAME=zzq_gobang

#项目路径
WORKDIR=/home/$USERNAME/ai_game_platform

#tmux session的名字
TMUX_RUN_SESSION_NAME=ai_game_workspace
TMUX_DEV_SESSION_NAME=ai_game_workspace_dev
result=$(tmux ls | grep $TMUX_RUN_SESSION_NAME)
echo "$result"

# tmux每开一个窗口，相当于新开了一个bash，每新开一个bash，就会执行整个脚本
# 所以每次执行脚本之前，应该判断一下这个脚本之前是否执行过，即判断tmux是否被创建出来
if [[ $result = "" ]]; then
  cd $WORKDIR || exit
  echo $USER_PASSWORD | sudo -S /etc/init.d/nginx start
  echo $USER_PASSWORD | sudo -S redis-server /etc/redis/redis.conf

  # 后台新建一个session
  tmux new-session -d -s $TMUX_RUN_SESSION_NAME
  # 向选择的窗口发送指令
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "uwsgi --ini scripts/uwsgi.ini" C-m

  tmux split-window -h
  tmux split-window -t $TMUX_RUN_SESSION_NAME:0.1 -v

  tmux split-window -t $TMUX_RUN_SESSION_NAME:0.0 -v
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "cd match_system/src/" C-m
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 main.py" C-m

  tmux split-window -t $TMUX_RUN_SESSION_NAME:0.0 -v
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "daphne -b 0.0.0.0 -p 5015 ai_game_platform.asgi:application" C-m
  tmux split-window -t $TMUX_RUN_SESSION_NAME:0.2 -v

  tmux new-session -d -s $TMUX_DEV_SESSION_NAME
  tmux split-window -h
  tmux split-window -t $TMUX_DEV_SESSION_NAME:0.1 -v
  tmux split-window -t $TMUX_DEV_SESSION_NAME:0.0 -v
  tmux send-keys -t $TMUX_DEV_SESSION_NAME:0.2 "python3 manage.py shell" C-m

  echo "66666666"
fi
