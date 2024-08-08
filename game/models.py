# models.py
from django.db import models
from django.contrib.auth.models import User


class ImageGame(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    pixelation_level = models.IntegerField(default=0)
    is_image_used = models.BooleanField(default=False)
    used_at = models.DateField(null=True, blank=True)


class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    played_matches = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"Statistics for {self.user.username}"


class UsedImageByUser(models.Model):
    image = models.ForeignKey(ImageGame, on_delete=models.CASCADE, unique=True)
    pixelation_level = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempts_history = models.TextField(default='')
    attempt_no = models.IntegerField(default=0)
    is_user_win = models.BooleanField(default=False)
    is_attempt_done = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
