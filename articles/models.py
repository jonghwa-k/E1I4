from django.db import models
from accounts.models import User

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='Ariticles/image/',null=True,blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title