from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class User(AbstractUser):
    nickname = models.CharField(
        max_length=30, 
        unique=True, 
        validators=[MinLengthValidator(3, "Nickname must be at least 3 characters long.")]
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(r'^(male|female|other)$', 'Gender must be male, female, or other.')]
    )
    bio = models.TextField(blank=True, null=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def follow(self, user):
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        if user != self:
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        return self.followers.filter(pk=user.pk).exists()