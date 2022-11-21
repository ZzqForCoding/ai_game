from rest_framework.views import APIView
from rest_framework.response import Response
from random import randint
from player.permissions.one_user_login import OneUserLogin

import base64
import time
import datetime
import json
import hmac
from hashlib import sha1 as sha

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
access_key_id = 'LTAI5tLM746uethTCU9J4BiA'
access_key_secret = 'zORXPhF7qvnhzGX95G54oM20K53V72'
# 填写Host地址，格式为https://bucketname.endpoint。
host = 'https://player-avatar.oss-cn-shenzhen.aliyuncs.com';
# 设置上传回调URL，即回调服务器地址，用于处理应用服务器与OSS之间的通信。OSS会在文件上传完成后，把文件上传信息通过此回调URL发送给应用服务器。
callback_url = "https://aigame.zzqahm.top/backend/player/img/receive/";
# 设置上传到OSS文件的前缀，可置空此项。置空后，文件将上传至Bucket的根目录下。
upload_dir = 'aigame_platform/avatar'
expire_time = 1000

class ApplyView(APIView):
    # permission_classes = ([OneUserLogin])

    def get(self, request):
        filename = request.GET.get('filename')
        userId = request.GET.get('userId')
        return Response(self.get_token(filename, userId))

    def get_iso_8601(self, expire):
        gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
        gmt += 'Z'
        return gmt


    def get_token(self, filename, userId):
        now = int(time.time())
        expire_syncpoint = now + expire_time
        expire = self.get_iso_8601(expire_syncpoint)
        policy_dict = {}
        policy_dict['expiration'] = expire
        condition_array = []
        array_item = []
        array_item.append('starts-with');
        array_item.append('$key');
        array_item.append(upload_dir);
        condition_array.append(array_item)
        policy_dict['conditions'] = condition_array
        policy = json.dumps(policy_dict).strip()
        policy_encode = base64.b64encode(policy.encode())
        h = hmac.new(access_key_secret.encode(), policy_encode, sha)
        sign_result = base64.encodestring(h.digest()).strip()

        callback_dict = {}
        callback_dict['callbackUrl'] = callback_url;
        callback_dict['callbackBody'] = 'filename=%s&userId=%s&randomname=${object}&size=${size}&mimeType=${mimeType}' \
                                        '&height=${imageInfo.height}&width=${imageInfo.width}' % (filename, userId);
        callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded';
        callback_param = json.dumps(callback_dict).strip()
        base64_callback_body = base64.b64encode(callback_param.encode());

        token_dict = {}
        token_dict['accessid'] = access_key_id
        token_dict['host'] = host
        token_dict['policy'] = policy_encode.decode()
        token_dict['signature'] = sign_result.decode()
        token_dict['expire'] = expire_syncpoint
        token_dict['dir'] = upload_dir
        token_dict['callback'] = base64_callback_body.decode()
        result = json.dumps(token_dict)
        return result
