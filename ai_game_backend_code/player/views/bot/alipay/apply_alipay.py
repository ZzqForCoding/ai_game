from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from alipay import AliPay
from player.permissions.one_user_login import OneUserLogin
from player.models.player import Player
from player.models.order import Order
from time import strftime, localtime
import random

class ApplyAliPayView(APIView):
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
        order = Order.objects.filter(user=request.user).first()

        if order and order.status in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return Response({
                'result': 'failed',
                'desp': "请勿重复支付!"
            })

        subject = "扩容Bot数量"
        out_trade_no = strftime('%Y%m%d%H%M%S' + str(random.randint(0, 1000)), localtime())
        trade_status = "WAIT_BUYER_PAY"
        player = Player.objects.get(user=request.user)
        order_string = self.alipay.api_alipay_trade_page_pay(
            # 订单号
            out_trade_no = out_trade_no,
            # 金额
            total_amount = "0.1",
            subject = subject,
            return_url = settings.ALIPAY_RETURN_URL % player.user.id,
            notify_url = settings.ALIPAY_ORDER_NOTIFY_URL
        )

        if order:
            order.status = "WAIT_BUYER_PAY"
            order.out_trade_no = out_trade_no
            order.save()
        else:
            order = Order.objects.create(user=request.user, out_trade_no=out_trade_no, amount=0.1, status=trade_status)
            order.save()

        pay_url = '%s?%s' % (settings.ALIPAY_URL, order_string)
        return Response({
            'result': 'success',
            'pay_url': pay_url
        })
