from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    GENDER_CHOICES = [
        ("남자", "남자"),
        ("여자", "여자"),
    ]
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    date_of_birth = models.DateField()
    subscription = models.BooleanField()

    REQUIRED_FIELDS = ["name", "nickname", "gender", "date_of_birth", "subscription"]