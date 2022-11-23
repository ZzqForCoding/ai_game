from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.platform_data import PlatformData
from player.models.player import Player
import datetime

class GetChartDataView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        user = request.user
        player = Player.objects.get(user=user)
        resp = {}

        cpp_skilled = 0
        if player.cpp_code_compile_cnt != 0:
            cpp_skilled = player.cpp_code_compile_success_cnt / player.cpp_code_compile_cnt
        py_skilled = 0
        if player.py_code_compile_cnt != 0:
            py_skilled = player.py_code_compile_success_cnt / player.py_code_compile_cnt
        java_skilled = 0
        if player.java_code_compile_cnt != 0:
            java_skilled = player.java_code_compile_success_cnt / player.java_code_compile_cnt

        resp['lang_skilled'] = [
            cpp_skilled,
            java_skilled,
            py_skilled
        ]
        today = datetime.date.today()
        pre_week = today - datetime.timedelta(days=6)
        register_cnts = []
        login_cnts = []
        dates = []
        for i in range((today - pre_week).days + 1):
            date = pre_week + datetime.timedelta(days=i)
            dates.append(date.strftime('%m.%d'))
            platform_data = PlatformData.objects.filter(date=date)
            if platform_data.exists():
                platform_data = platform_data.first()
                register_cnts.append(platform_data.register_cnt)
                login_cnts.append(platform_data.login_cnt)
            else:
                register_cnts.append(0)
                login_cnts.append(0)
        resp['dates'] = dates
        resp['register_cnts'] = register_cnts
        resp['login_cnts'] = login_cnts
        resp['result'] = 'success'
        return Response(resp)




