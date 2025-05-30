# filemanager/models.py (Updated)
from django.db import models
from admins.models import AdminUser

class SystemFile(models.Model):
    """Files created by admin for system purposes - no user data"""
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='admin_files/')
    file_type = models.CharField(max_length=50)  # 'backup', 'export', 'report'
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file_type}: {self.description}"

class ExportJob(models.Model):
    """Track export jobs without storing user data"""
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    export_type = models.CharField(max_length=50)  # 'user_stats', 'system_health'
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    file = models.ForeignKey(SystemFile, on_delete=models.CASCADE, null=True, blank=True)