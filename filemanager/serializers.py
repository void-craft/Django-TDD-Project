from rest_framework import serializers
from .models import SystemFile  # Change from UploadedFile

class ManagedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemFile
        fields = ['id', 'owner', 'file', 'description', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']