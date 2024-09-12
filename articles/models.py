from django.db import models
from accounts.models import User

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    url = models.URLField(null=True,blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='Ariticles/image/',null=True,blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class ArticleLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_a")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes_a")


class CommentLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_c")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes_c")