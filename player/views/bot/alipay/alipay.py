from rest_framework.views import APIView
from rest_framework.response import Response
from player.permissions.one_user_login import OneUserLogin
from django.conf import settings
from alipay import AliPay
from time import strftime, localtime
import json
import random

class AliPayView(APIView):
    # permission_classes = ([OneUserLogin])

    def __init__(self):
        self.app_private_key_string = open(settings.ALIPAY_KEY_DIR + 'app_private_key.pem').read()
        self.alipay_public_key_string = open(settings.ALIPAY_KEY_DIR + 'alipay_public_key.pem').read()
        self.alipay = alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,    # 默认回调url
            app_private_key_string=self.app_private_key_string,
            alipay_public_key_string=self.alipay_public_key_string,
            sign_type='RSA2',
            debug=True,
        )
        self.return_url = settings.RETURN_URL

    def post(self, request):
        subject = "扩容Bot数量"
        order_string = self.alipay.api_alipay_trade_page_pay(
            # 订单号
            out_trade_no = strftime('%Y%m%d%H%M%S' + str(random.randint(0, 1000)), localtime()),
            # 金额
            total_amount = "0.1",
            subject = subject,
            return_url = self.return_url
        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return Response({
            'result': 'success',
            'pay_url': pay_url
        })

    def get_trade_result(self, order_id):
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False

    def get_verify_result(self, data, sign):
        return self.alipay.verify(data, sign)
