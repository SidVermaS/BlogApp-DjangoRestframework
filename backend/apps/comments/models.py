from django.db import models
from core.base import BaseModel
from apps.posts.models import Post
from apps.profiles.models import Profile

class Comment(BaseModel):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text