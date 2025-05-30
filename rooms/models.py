from django.db import models
from users.models import CustomUser

class Room(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rooms')
    name  = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.name}’s {self.name}"

class Thing(models.Model):
    room       = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='things')
    name       = models.CharField(max_length=100)
    quantity   = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"
