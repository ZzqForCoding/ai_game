import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_game_platform.settings")
django.setup()  # os.environ['DJANGO_SETTINGS_MODULE']

from django.core.cache import cache
from ai_game_platform.asgi import channel_layer
from asgiref.sync import async_to_sync
import pika
import random
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

def main():
    credentials = pika.PlainCredentials('zzq', 'zxc123')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672,
        credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue='notification_queue', durable=True)

    ali_credential = AccessKeyCredential('LTAI5t5deyvqJMKrSMVCj6Kx', 'IIqFp7GKU5Nap7kpxLyrKLKjY9sJvc')
    client = AcsClient(region_id='cn-shenzhen', credential=ali_credential)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
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
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume('notification_queue', on_message_callback=callback)

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
