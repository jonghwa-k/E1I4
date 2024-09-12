from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class User(AbstractUser):
    nickname = models.CharField(
        max_length=30, 
        unique=True, 
        validators=[MinLengthValidator(3, "Nickname must be at least 3 characters long.")]
    )

    bio = models.TextField(blank=True, null=True)


    is_active = models.BooleanField(default=True)  # Standard field for deactivating accounts
    deactivation_date = models.DateTimeField(null=True, blank=True)  # Stores the date of deactivation

