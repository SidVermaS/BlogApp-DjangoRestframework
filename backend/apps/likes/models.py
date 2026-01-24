from django.db import models
from core.base import BaseModel
from apps.posts.models import Post
from apps.profiles.models import Profile

class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'likes', db_index = True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes', db_index=True)

    class Meta:
        db_table = 'likes'
        constraints=[
            models.UniqueConstraint(
                fields=['post','profile'],
                name='unique_post_profile_like'
            )
        ]

    def __str__(self):
        return f"post_id: {self.post.id} profile_id: {self.profile.id}"