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

    apply_access_token_url = "https://www.acwing.com/third_party/api/oauth2/access_token/"
    params = {
        'appid': "3381",
        'secret': "6ca382716fda427e82b5035d3f8a7e95",
        'code': code
    }

    access_token_res = requests.get(apply_access_token_url, params=params).json()

    access_token = access_token_res['access_token']
    openid = access_token_res['openid']

    players = Player.objects.filter(openid=openid)
    if player.exists():
        refresh = RefreshToken.for_user(players[0].user)
        return JsonResponse({
            'result': "success",
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    get_userinfo_url = "https://www.acwing.com/third_party/api/meta/identity/getinfo/"
    params = {
        'access_token': access_token,
        'openid': openid
    }
    userinfo_res = requests.get(get_userinfo_url, params=params).json()
    username = userinfo_res['username']
    photo = userinfo_res['photo']

    users = User.objects.filter(username=username, photo=photo)
    while users.exist():
        players = Player.objects.filter(user=users[0])
        if players.exists():
            player = players[0]
            refresh = RefreshToken.for_user(player.user)
            return JsonResponse({
                'result': "success",
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })

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
