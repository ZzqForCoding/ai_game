from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from player.models.img import Img

class ReceiveView(APIView):

    def post(self, request):
        data =  request.POST
        user = User.objects.get(id=data['userId'])
        img = Img.objects.create(user=user, filename=data['filename'], randomname=data['randomname'], size=data['size'],
                mimetype=data['mimeType'], height=data['height'], width=data['width'], url='https://img.zzqahm.top/%s' %
                data['randomname'])
        img.save()
        return Response({
            'result': "success",
            'imgId': img.id,
            'imgName': img.filename,
            'imgUrl': img.url
        })
