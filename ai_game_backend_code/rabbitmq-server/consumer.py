
import pika
import sys, os
import random
import json
import django

from django.core.cache import cache
from asgiref.sync import async_to_sync

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

from heartbeat import Heartbeat

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_game_platform.settings")
django.setup()  # os.environ['DJANGO_SETTINGS_MODULE']

from ai_game_platform.asgi import channel_layer
from ai_game_platform import settings
import secret

def main():
    credentials = pika.PlainCredentials('zzq', 'zxc123')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672,
        credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue=settings.QUEUE, durable=True)

    def send_msg_callback(data, properties):
        request = SendSmsRequest()
        request.set_accept_format('json')
        request.set_PhoneNumbers(data['phone'])
        request.set_SignName("zzq的开发日记")
        code = random.randint(1000, 9999)
        request.set_TemplateCode("SMS_259640123")
        request.set_TemplateParam("{\"code\":\"%d\"}" % code)

        lenth = len(secret.ACCESS_KEY_ID)
        flag = False
        for i in range(lenth):
            ali_credential = AccessKeyCredential(secret.ACCESS_KEY_ID[i], secret.ACCESS_KEY_SECRET[i])
            client = AcsClient(region_id='cn-shenzhen', credential=ali_credential)
            response = client.do_action_with_exception(request)
            response = json.loads(response.decode())
            if response["Code"] == "OK":
                cache.set(data['phone'], code, 5 * 60)
                flag = True
        if not flag:
            body = {
                "event": "verifycode_error",
                "target_user_id": data['target_user_id'],
                "data": {
                    "msg": "点击太过频繁，请换个时间或方式登录吧!",
                }
            }
            print("click buisy: %s" % data['phone'])
            channel.basic_publish(exchange='', routing_key=settings.QUEUE, body=json.dumps(body),
                    properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    def notification_callback(data):
        channel_name = 'notification_%d' % data['target_user_id']
        is_online = str(cache.get(channel_name))
        if is_online:
            async_to_sync(channel_layer.group_send) (
                channel_name,
                {
                    'type': 'group_send_event',
                    'event': data['event'],
                    'data': data['data'],
                }
            )

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        if data['event'] == settings.SEND_MSG_EVENT:
            send_msg_callback(data, properties)
        elif data['event'] in settings.NOTIFICATION_EVENT:
            notification_callback(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(settings.QUEUE, on_message_callback=callback)

    # 开启心跳线程
    heartbeat = Heartbeat(connection)
    heartbeat.start()
    heartbeat.startHeartbeat()

    print(' [*] Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
