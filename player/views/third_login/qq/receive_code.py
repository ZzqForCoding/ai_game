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
        'client_id': "",
        'client_secret': "",
        'redirect_uri': "https://aigame.zzqahm.top/backend/player/qq/receive_code",
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
        refresh = RefreshToken.for_user(players[0].user)
        return JsonResponse({
            'result': "success",
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    get_userinfo_url = "https://graph.qq.com/user/get_user_info"
    params = {
        'access_token': access_token,
        'oauth_consumer_key': "",
        'openid': openid
    }
    userinfo_res = requests.get(get_userinfo_url, params=params).json()
    username = userinfo_res["nickname"]
    photo = userinfo_res["figureurl_qq_1"]

    while User.objects.filter(username=username).exists():
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    refresh = RefreshToken.for_user(players[0].user)
    return JsonResponse({
        'result': "success",
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })
