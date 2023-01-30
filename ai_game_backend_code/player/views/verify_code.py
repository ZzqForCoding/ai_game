from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from random import randint

class VerifyCodeView(APIView):
    def get_state(self):
        res = ""
        for i in range(8):
            res += str(randint(0, 9))
        return res

    def post(self, request):
        data = request.POST
        phone = data.get('phone', '')
        code = data.get('code', '')
        cache_code = str(cache.get(phone, ''))
        if code != cache_code:
            return Response({
                'result': "验证码不一致"
            })
        else:
            state = self.get_state()
            cache.set(state, phone, 5 * 60)
            cache.delete(phone)
            return Response({
                'result': "success",
                'state': state,
            })
