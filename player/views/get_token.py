from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from player.models.player import Player

class RemTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        player = Player.objects.filter(user=self.user)[0]
        player.token = "Bearer %s" % (data['access'])
        player.save()
        return data

class RemTokenObtainPairView(TokenObtainPairView):
    serializer_class = RemTokenObtainPairSerializer
