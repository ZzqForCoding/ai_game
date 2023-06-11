from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth.models import User
from ai_game_platform import settings
from player.models.player import Player
from player.models.platform_data import PlatformData
from random import randint
from datetime import date
import datetime
import requests
import pika
import json

def receive_code(request):
    data = request.GET
    code = data.get('code')
    state = data.get('state')

    if not cache.has_key(state):
        return JsonResponse({
            'result': "failed"
        })

    cache.delete(state)

    apply_access_token_url = "https://graph.qq.com/oauth2.0/token"
    params = {
        'grant_type': "authorization_code",
        'client_id': "102024822",
        'client_secret': "30jGZgZGiz1sUu54",
        'code': code,
        'redirect_uri': "https://aigame.zzqahm.top/player/qq/receive_code",
        'fmt': "json"
    }
    access_token_res = requests.get(apply_access_token_url, params=params).json()
    access_token = access_token_res['access_token']

    get_user_openid_url = "https://graph.qq.com/oauth2.0/me"
    params = {
        'access_token': access_token,
        'fmt': "json"
    }
    openid_res = requests.get(get_user_openid_url, params=params).json()
    openid = openid_res['openid']

    players = Player.objects.filter(openid=openid)
    if players.exists():
        player = players[0]

        # 若当前已在线，则通知给用户
        is_online = cache.get('notification_%d' % player.user.id, '')
        if is_online:
            credentials = pika.PlainCredentials('zzq', 'zxc123')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',
                port=5672, credentials=credentials))
            channel = connection.channel()
            body = {
                'event': settings.NOTIFICATION_EVENT[0],
                'target_user_id': player.user.id,
                'data': {
                    'title': "[通知] 帐号异常",
                    'msg': '您的帐号再别的地方登陆，若不是您请修改密码',
                },
            }
            channel.basic_publish(exchange='', routing_key=settings.QUEUE, body=json.dumps(body),
                    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
            connection.close()

        refresh = RefreshToken.for_user(player.user)
        token = str(refresh.access_token)
        refresh = str(refresh)
        player.token = "Bearer %s" % (token)
        player.save()
        # 记录登录人数
        users = cache.get('login_users', [])
        if player.user.id not in users:
            today = datetime.date.today()
            platformData = PlatformData.objects.filter(date=today)
            if not platformData.exists():
                platformData = PlatformData.objects.create(date=today, login_cnt=1)
            else:
                platformData = platformData.first()
                platformData.login_cnt += 1
            platformData.save()
            users.append(player.user.id)
            st = datetime.datetime.now()
            ed = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.datetime.min.time())
            cache.set('login_users', users, (ed - st).seconds)
        return JsonResponse({
            'result': "success",
            'access': token,
            'refresh': refresh
        })

    get_userinfo_url = "https://graph.qq.com/user/get_user_info"
    params = {
        'access_token': access_token,
        'oauth_consumer_key': "102024822",
        'openid': openid
    }
    userinfo_res = requests.get(get_userinfo_url, params=params).json()
    username = userinfo_res["nickname"]
    photo = userinfo_res["figureurl_qq_1"]

    while User.objects.filter(username=username).exists():
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    refresh = RefreshToken.for_user(player.user)
    token = str(refresh.access_token)
    refresh = str(refresh)
    player.token = "Bearer %s" % token
    player.save()

    # 记录注册人数
    today = date.today()
    platformData = PlatformData.objects.filter(date=today)
    if not platformData.exists():
        platformData = PlatformData.objects.create(date=today, register_cnt=1)
    else:
        platformData = platformData.first()
        platformData.register_cnt += 1
    platformData.save()

    return JsonResponse({
        'result': "success",
        'access': token,
        'refresh': refresh
    })
