from django.http import HttpResponse, JsonResponse

def index(request):
    resp = {
        'username': 'zzq',
        'age': 28,
        'sex': '男'
    }
    return JsonResponse(resp)
