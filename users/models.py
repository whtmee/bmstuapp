from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='users_image/', default='avatars/default.png', verbose_name='Аватар')
    
    def __str__(self):
        return f"Профиль {self.username}"
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'