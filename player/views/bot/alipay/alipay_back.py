from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from alipay import AliPay
from player.permissions.one_user_login import OneUserLogin
from player.models.order import Order

class AliPayBackView(APIView):
    # permission_classes = ([OneUserLogin])

    def __init__(self, **kwargs):
        self.app_private_key_string = open(settings.ALIPAY_KEY_DIR + 'app_private_key.pem').read()
        self.alipay_public_key_string = open(settings.ALIPAY_KEY_DIR + 'alipay_public_key.pem').read()
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,    # 默认回调url
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type='RSA2',
            debug=settings.ALIPAY_DEBUG,
        )

    def post(self, request):
        data = request.data.copy()
        data = data.dict()
        signature = data.pop('sign')
        success = self.alipay.verify(data, signature)

        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            out_trade_no = data['out_trade_no']
            trade_id = data['trade_no']
            pay_order = Order.objects.filter(out_trade_no=out_trade_no).first()
            pay_order.status = data["trade_status"]
            pay_order.trade_id = trade_id
            pay_order.save()
            return Response({
                'result': "success",
                'desp': "支付成功!"
            })
        else:
            return Response({
                'result': 'failed',
                'desp': "支付失败!"
            })
