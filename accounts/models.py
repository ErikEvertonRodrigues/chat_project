from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User Account")
    avatar = models.ImageField(upload_to="profile/avatar/", null=True, blank=True, verbose_name="User Biography")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
