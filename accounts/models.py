from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='avatars/',
        default='icons/default_avatar.png',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True
    )
    address = models.TextField(max_length=200, blank=True, verbose_name='送貨地址')
    
    def __str__(self):
        return f"{self.user.username} 的個人資料"

    class Meta:
        verbose_name = '用戶個人資料'
        verbose_name_plural = '用戶個人資料'