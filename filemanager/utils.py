# filemanager/utils.py
import logging
from django.utils import timezone

admin_logger = logging.getLogger('admin_actions')

def log_admin_action(admin_user, action, details=None):
    """Log admin actions without exposing user data"""
    admin_logger.info(f"Admin {admin_user.user.email} performed {action}", 
                     extra={'details': details or {}})

def create_anonymized_export(export_type, admin_user):
    """Create exports with anonymized data only"""
    admin_logger.info(f"Export requested: {export_type} by {admin_user.user.email}")
    pass