# admins/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import CustomUser

class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='admin')
    permissions = models.JSONField(default=dict)  # For granular permissions
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Admin: {self.user.email}"

class AdminActivity(models.Model):
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)  # Non-sensitive metadata only
    
    class Meta:
        ordering = ['-timestamp']