from django.core.cache import cache
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User
from player.models.player import Player
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken

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
        refresh = RefreshToken.for_user(player.user)
        token = str(refresh.access_token)
        refresh = str(refresh)
        player.token = "Bearer %s" % (token)
        player.save()
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
