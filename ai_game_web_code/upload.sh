#! /bin/bash

ssh zzq 'cd /home/zzq/ai_game/ai_game_backend_code && ./scripts/del_web.sh'

scp -r dist/* zzq:/home/zzq/ai_game/ai_game_backend_code/web/
