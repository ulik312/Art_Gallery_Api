from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from account.models import MyUser
from likes.models import Like


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Rating(models.Model):
    RATE_CHOICES = (
        (4, "excellent"),
        (3, "very good"),
        (2, "good"),
        (1, "bad"),
    )

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=0)



class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

