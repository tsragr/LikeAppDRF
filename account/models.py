from django.db import models
from django.contrib.auth.models import User
from account.services import user_directory_path


class Account(models.Model):
    """
    Basic user's account model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    avatar = models.ImageField(upload_to=user_directory_path)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
