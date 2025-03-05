from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    pub_datetime = models.DateTimeField('date published', db_index=True)
    status = models.SmallIntegerField(default=0) # 0 - unpublished 1 - publihsed 2 - error
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to='post_images/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
