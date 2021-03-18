from django.db import models

from account.models import MyUser
from main.models import Post


class Favourite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=True)
