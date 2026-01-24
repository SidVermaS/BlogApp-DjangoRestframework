from django.db import models
from backend.core.base import BaseModel
from backend.apps.profiles import Profile

class Post(BaseModel):
    title = models.CharField(max_length = 100, unique = True, db_index = True)
    content = models.TextField()
    image = models.ImageField(upload_to = 'posts/images/%Y/%m/%d/', null = True, blank = True)
    likes_count = models.PositiveIntegerField(default = 0, null = False)
    comments_count = models.PositiveIntegerField(default = 0, null = False)

    author = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = "posts",  db_index = True)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title