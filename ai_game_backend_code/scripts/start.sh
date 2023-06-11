#! /bin/bash

#项目路径
WORKDIR=/code

#tmux session的名字
TMUX_RUN_SESSION_NAME=ai_game_backend_workspace
TMUX_DEV_SESSION_NAME=ai_game_backend_workspace_dev

sudo service rabbitmq-server start
rabbitmqctl add_user zzq zxc123
rabbitmqctl set_user_tags zzq administrator
rabbitmqctl set_permissions -p / zzq ".*" ".*" ".*"

cd $WORKDIR || exit


# 后台新建一个session
tmux new-session -d -s $TMUX_RUN_SESSION_NAME
# 分割窗口
tmux split-window -h # 横向分割
tmux select-pane -t 1
tmux split-window -v
tmux split-window -v
tmux select-pane -t 1
tmux split-window -v
tmux select-pane -t 5
tmux split-window -v
tmux split-window -v
tmux select-pane -t 5
tmux split-window -v
tmux select-pane -t 7
tmux split-window -h
tmux select-pane -t 9
tmux split-window -h

# 向选择的窗口发送指令
tmux select-pane -t 8
tmux send-keys -t $TMUX_RUN_SESSION_NAME "sudo /etc/init.d/nginx start" C-m
tmux select-pane -t 9
tmux send-keys -t $TMUX_RUN_SESSION_NAME "sudo /etc/init.d/redis-server start" C-m
tmux select-pane -t 10
tmux send-keys -t $TMUX_RUN_SESSION_NAME "sudo service rabbitmq-server start" C-m
tmux select-pane -t 6
tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 manage.py shell" C-m
tmux send-keys -t $TMUX_RUN_SESSION_NAME "from django.core.cache import cache" C-m
tmux send-keys -t $TMUX_RUN_SESSION_NAME "cache.keys('*')" C-m
tmux send-keys -t $TMUX_RUN_SESSION_NAME "cache.clear()" C-m
tmux send-keys -t $TMUX_RUN_SESSION_NAME "cache.has_key('')" C-m
tmux select-pane -t 7
tmux send-keys -t $TMUX_RUN_SESSION_NAME "./scripts/compress_game_js.sh" C-m
tmux select-pane -t 1
tmux send-keys -t $TMUX_RUN_SESSION_NAME "uwsgi --ini scripts/uwsgi.ini" C-m
tmux select-pane -t 2
tmux send-keys -t $TMUX_RUN_SESSION_NAME "daphne -b 0.0.0.0 -p 5015 ai_game_platform.asgi:application" C-m
tmux select-pane -t 3
tmux send-keys -t $TMUX_RUN_SESSION_NAME "cd match_system/src/" C-m
tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 main.py" C-m
tmux select-pane -t 4
tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 rabbitmq-server/consumer.py" C-m
tmux select-pane -t 5
tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 rabbitmq-server/consumer.py" C-m

tmux new-session -d -s $TMUX_DEV_SESSION_NAME
tmux split-window -h
tmux split-window -v
tmux select-pane -t 2
tmux send-keys -t $TMUX_DEV_SESSION_NAME "python3 manage.py shell" C-m

echo "66666666"

tail -f /dev/null
