from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


class ImageUploader(models.Model):
    image_name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Images')
    user = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)