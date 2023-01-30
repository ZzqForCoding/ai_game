#! /bin/bash

ssh aigame 'cd /code/backend_venv && ./scripts/del_web.sh'

scp -r dist/* aigame:/code/backend_venv/web/
