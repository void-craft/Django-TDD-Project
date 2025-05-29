from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ThingViewSet, shopping_list

# First, define any standalone URL patterns
urlpatterns = [
    path('shopping-list/', shopping_list, name='shopping-list'),
]

# Then, set up the router and register viewsets
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'things', ThingViewSet, basename='thing')

# Finally, append router URLs to the urlpatterns
urlpatterns += router.urls
