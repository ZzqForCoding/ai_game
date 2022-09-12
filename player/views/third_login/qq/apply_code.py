from django.http import JsonResponse
from urllib.parse import quote
from random import randint
from django.core.cache import cache

def get_state():
    res = ""
    for i in range(8):
        res += str(randint(0, 9))
    return res

def apply_code(request):
    response_type = "code"
    client_id = ""
    redirect_uri = quote("https://aigame.zzqahm.top/player/qq/receive_code")
    scope = "get_user_info"
    state = get_state()
    cache.set(state, True, 7200)

    apply_code_url = "https://graph.qq.com/oauth2.0/authorize"
    return JsonResponse({
        'result': "success",
        'apply_code_url': apply_code_url + "?response_type=%s&client_id=%s&redirect_uri=%s&scope=%s&state=%s" % (response_type, client_id, redirect_uri, scope, state)
    })


