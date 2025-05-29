from django.urls import path
from . import views
from users.views import UserDetail, UserList

urlpatterns = [
    path('', views.UserList.as_view(), name='user-list'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetail.as_view(), name='user-detail'),
]
