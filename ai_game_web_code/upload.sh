#! /bin/bash

ssh aigame 'cd /code && ./scripts/del_web.sh'

scp -r dist/* aigame:/code/web/
