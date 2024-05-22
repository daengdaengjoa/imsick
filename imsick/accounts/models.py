# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    introduction = models.CharField(max_length=500, blank=True, null=True)
    score = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # 수동으로 date_joined 필드 추가
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # related_name 수정
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                    'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',  # related_name 수정
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )
