#! /bin/bash
#项目路径
WORKDIR=/code

#tmux session的名字
TMUX_RUN_SESSION_NAME=code_runner_workspace
cd $WORKDIR || exit

# 后台新建一个session
tmux new-session -d -s $TMUX_RUN_SESSION_NAME
# 分割窗口
tmux split-window -h # 横向分割
tmux select-pane -t 1
tmux split-window -v
tmux select-pane -t 3
tmux split-window -v

# 向选择的窗口发送指令
tmux select-pane -t 1
tmux send-keys -t $TMUX_RUN_SESSION_NAME "rm .main.py.swp" C-m
tmux select-pane -t 2
tmux send-keys -t $TMUX_RUN_SESSION_NAME "rm .sandbox.py.swp" C-m
tmux select-pane -t 3
tmux send-keys -t $TMUX_RUN_SESSION_NAME "python3 main.py" C-m

echo "66666666"

tail -f /dev/null
