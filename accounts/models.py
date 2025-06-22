from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # 確保即使信號多次觸發，也不重複創建
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)