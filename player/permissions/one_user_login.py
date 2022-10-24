from rest_framework import permissions
from player.models.player import Player

class OneUserLogin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        token = request.META.get("HTTP_AUTHORIZATION")
        player = Player.objects.filter(user=user)[0]
        if player.token == str(token):
            return True
        return False
