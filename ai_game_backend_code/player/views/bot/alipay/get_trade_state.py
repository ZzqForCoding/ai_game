from rest_framework.view import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from player.models.order import Order

class GetTradeStateView(APIView):
    permission_classes = ([OneUserLogin])

    def get(self, request, out_trade_no):
        order = Order.objects.get(out_trade_no=out_trade_no)
        if order.status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return Response({'result': "success"})
        else:
            return Response({'result': "failed"})
