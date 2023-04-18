from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="likes")
    
    def LikeCount(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-datetime']
        
    def __str__(self):
        return f"{self.user}: {self.content}"
        
class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="following")
    followedby = models.ManyToManyField(User, symmetrical=False, blank=True, related_name="followedby")
    
    def FollowCount(self):
        return self.following.count()
    
    def FollowedByCount(self):
        return self.followedby.count()