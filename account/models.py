from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    email = models.EmailField('Email', max_length=50)
    telegram = models.CharField('Telegram', max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
