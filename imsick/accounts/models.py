from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractUser):
    GENDER_CHOICES = [("M", "M"),("W", "W")]
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=1)
    point =  models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], default=0)
    

    REQUIRED_FIELDS = ["name", "nickname", "gender", "age", "point"]