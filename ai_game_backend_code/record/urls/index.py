from django.urls import path
from record.views.getlist import GetListView
from record.views.getlist_userid import GetListForUserIdView

urlpatterns = [
    path('getlist/', GetListView.as_view(), name='record_getlist'),
    path('getlist/<int:userId>/', GetListForUserIdView.as_view(), name='record_getlist_userid'),
]
