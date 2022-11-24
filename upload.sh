#! /bin/bash

ssh gobang 'cd ai_game_platform && ./scripts/del_web.sh'

scp -r dist/* gobang:ai_game_platform/web/
