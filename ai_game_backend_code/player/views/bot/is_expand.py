from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions.one_user_login import OneUserLogin
from player.models.order import Order

class IsExpandView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request):
        user = request.user
        order = Order.objects.filter(user=user).first()
        if order and order.status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return Response({
                'result': "success",
                'status': True,
            })
        return Response({
            'result': "success",
            'status': False
        })
