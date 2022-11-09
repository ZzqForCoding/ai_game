from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from django.conf import settings

class AliPayBackView(APIView):
    def get(self, request):
        data = request.data
        data.pop('sign')
        print(data)
        return Response({
            'result': "success"
        })
