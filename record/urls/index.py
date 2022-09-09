from django.urls import path
from record.views.getlist import GetListView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='record_getlist'),
]
