#! /bin/bash
USER_PASSWORD=123
USERNAME=zzq_code

#项目路径
WORKDIR=/home/$USERNAME/code_runner_system/src

echo $USER_PASSWORD | sudo -S chmod 666 /var/run/docker.sock

#tmux session的名字
TMUX_RUN_SESSION_NAME=code_runner_workspace
result=$(tmux ls | grep $TMUX_RUN_SESSION_NAME)
echo "$result"

# tmux每开一个窗口，相当于新开了一个bash，每新开一个bash，就会执行整个脚本
# 所以每次执行脚本之前，应该判断一下这个脚本之前是否执行过，即判断tmux是否被创建出来
if [[ $result = "" ]]; then
  cd $WORKDIR || exit

  # 后台新建一个session
  tmux new-session -d -s $TMUX_RUN_SESSION_NAME
  # 向选择的窗口发送指令
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "vim main.cpp" C-m

  tmux split-window -h
  tmux send-keys -t $TMUX_RUN_SESSION_NAME "./main" C-m
  tmux split-window -t $TMUX_RUN_SESSION_NAME:0.1 -v

  echo "66666666"
fi
