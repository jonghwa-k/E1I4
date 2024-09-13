from django.db import models
from django.utils import timezone
from accounts.models import User


# 고정된 카테고리 선택지
CATEGORY_CHOICES = [
    ('News', 'News'),
    ('자유게시판', '자유게시판'),
]

# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    url = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='Ariticles/image/',null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='News')
    likes = models.ManyToManyField(User, related_name="like_article", blank=True)

    def total_likes(self):
        return self.likes.count()
        
    def __str__(self):
        return self.title



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_comment", blank=True)

    def __str__(self):
        return f'{self.author.username}의 댓글'