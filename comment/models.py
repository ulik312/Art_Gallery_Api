from django.db import models

from account.models import MyUser
from main.models import Post


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING,related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}: {self.body}'

    class Meta:
        ordering = ('-created',)
