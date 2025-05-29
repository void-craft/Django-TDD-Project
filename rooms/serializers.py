from rest_framework import serializers
from .models import Room, Thing

class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Thing
        fields = ['id', 'name', 'quantity']

class RoomSerializer(serializers.ModelSerializer):
    things = ThingSerializer(many=True, read_only=True)
    class Meta:
        model  = Room
        fields = ['id', 'name', 'things']
