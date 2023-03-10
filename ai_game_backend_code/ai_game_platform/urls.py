"""ai_game_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/player/', include("player.urls.index")),
    path('backend/game/', include("game.urls.index")),
    path('backend/record/', include("record.urls.index")),
    path('backend/playervoice/', include("player_voice.urls.index")),
    path('backend/doc/', include_docs_urls(title="AIGame Platform接口文档", description="游戏编程对战平台API文档")),
]
